from api.tools.calc1040 import calc_1040

def test_standard_deduction_single():
    result = calc_1040(50000, "single")
    assert result["taxable_income"] == 50000 - 14600
    assert result["tax"] >= 0
