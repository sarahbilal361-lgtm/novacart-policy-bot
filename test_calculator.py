from calculator import (
    percent_of, gst_included, code_discount, split_discount, refund_calc,
)


def test_half_up_not_bankers():
    assert percent_of(25, 10) == 3      # 2.5 -> 3 (Python round() would give 2)
    assert percent_of(35, 10) == 4      # 3.5 -> 4


def test_gst():
    assert gst_included(1180) == 180


def test_file12_worked_example():
    # file 12 s6.4: TECH500 on 5000, 5000, 5500 -> shares 161, 161, 178
    d = code_discount(15500, flat_amount=500, max_discount=500, min_subtotal=15000)
    assert d == {"discount": 500, "minimum_met": True}
    assert split_discount([5000, 5000, 5500], 500) == [161, 161, 178]


def test_minimum_not_met():
    assert code_discount(2999, rate_percent=10, max_discount=1000, min_subtotal=3000) == {
        "discount": 0, "minimum_met": False}


def test_percentage_cap():
    # WELCOME10 on Rs. 20,000 -> 2,000 capped at 1,000
    assert code_discount(20000, rate_percent=10, max_discount=1000, min_subtotal=3000)["discount"] == 1000


def test_tie_goes_to_first_listed():
    shares = split_discount([100, 100, 100], 100)   # 33,33,33 -> diff 1 to first
    assert shares == [34, 33, 33]


def test_refund_never_negative():
    r = refund_calc([100], [0], 200)
    assert r["refund_total"] == 0


def test_refund_opened_electronics():
    # paid 10,000, opened, 15% restocking = 1,500, return label Rs. 200
    r = refund_calc([10000], [15], 200)
    assert r["restocking_fees"] == [1500]
    assert r["refund_total"] == 8300
