"""NovaCart calculators.

All money maths lives here so the LLM never does arithmetic itself.
Rules implemented:
- file 00 s1.3: amounts are rounded HALF UP to whole rupees at the moment they are
  computed; decimals are never carried into a later step.
- file 00 s1.2: GST inside a GST-inclusive price = price * 18 / 118.
- file 12 s3.2-3.3: code discount, capped by the maximum and by the eligible subtotal.
- file 12 s6.1-6.2: discount split across items, rounding difference goes to the
  most expensive item (first listed wins a tie).
- file 01 s5.2-5.3: refund per item = paid price - restocking fee; refund total =
  sum of item refunds - ONE return fee, never below Rs. 0.
"""
from decimal import Decimal, ROUND_HALF_UP


def _half_up(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def percent_of(amount: int, percent: float) -> int:
    """Return percent% of amount in whole rupees, rounded half up.

    Example: percent_of(25, 10) -> 3 (2.5 rounds up).
    """
    return _half_up(Decimal(str(amount)) * Decimal(str(percent)) / Decimal(100))


def gst_included(price: int) -> int:
    """GST contained in a GST-inclusive price (price * 18 / 118, rounded half up)."""
    return _half_up(Decimal(str(price)) * Decimal(18) / Decimal(118))


def code_discount(
    eligible_subtotal: int,
    rate_percent: float = 0,
    flat_amount: int = 0,
    max_discount: int = 0,
    min_subtotal: int = 0,
) -> dict:
    """Discount for a promo code on the ELIGIBLE subtotal (file 12 s3).

    Use rate_percent (and max_discount) for percentage codes such as WELCOME10 or
    STYLE15. Use flat_amount for TECH500. min_subtotal is the code's minimum eligible
    subtotal. If the minimum is not met the discount is 0.
    Returns {"discount": int, "minimum_met": bool}.
    """
    if eligible_subtotal < min_subtotal:
        return {"discount": 0, "minimum_met": False}
    if rate_percent:
        discount = percent_of(eligible_subtotal, rate_percent)
        if max_discount:
            discount = min(discount, max_discount)
    else:
        discount = flat_amount
    discount = min(discount, eligible_subtotal)
    return {"discount": discount, "minimum_met": True}


def split_discount(prices: list[int], discount: int) -> list[int]:
    """Split a code discount across eligible items by price (file 12 s6.1-6.2).

    prices must be the selling prices of the ELIGIBLE items in the order they are
    listed in the order. Returns each item's share of the discount.
    """
    total = sum(prices)
    if total == 0:
        return [0 for _ in prices]
    shares = [
        _half_up(Decimal(discount) * Decimal(p) / Decimal(total)) for p in prices
    ]
    diff = discount - sum(shares)
    if diff != 0:
        # most expensive item gets the difference; first listed wins a tie
        idx = max(range(len(prices)), key=lambda i: (prices[i], -i))
        shares[idx] += diff
    return shares


def refund_calc(
    paid_prices: list[int],
    restock_percents: list[float],
    return_fee: int,
) -> dict:
    """Refund for one return request (file 01 s5).

    paid_prices: paid price of each returned item (selling price minus its share of
        any code discount, or its share of a bundle price).
    restock_percents: restocking fee percent for each item, same order
        (0 if none, 15 for opened electronics, 10 for non-defective furniture/bulky).
    return_fee: the ONE fee for the request (Rs. 200, Rs. 2,000, Rs. 400 remote,
        or 0 for a NovaCart error return).
    Returns per-item restocking fee and refund, and the refund total (never below 0).
    """
    fees = [percent_of(p, pct) for p, pct in zip(paid_prices, restock_percents)]
    item_refunds = [p - f for p, f in zip(paid_prices, fees)]
    total = max(0, sum(item_refunds) - return_fee)
    return {
        "restocking_fees": fees,
        "item_refunds": item_refunds,
        "return_fee": return_fee,
        "refund_total": total,
    }
