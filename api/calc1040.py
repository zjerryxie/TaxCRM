def calc_1040(income: float, filing_status: str = "single") -> dict:
    """
    Simplified 1040 calculator (for demo only)
    - Standard deduction only
    - 2024 brackets
    """

    standard_deduction = {
        "single": 14600,
        "married": 29200
    }.get(filing_status, 14600)

    taxable_income = max(0, income - standard_deduction)

    brackets = [
        (11000, 0.10),
        (44725, 0.12),
        (95375, 0.22),
        (182100, 0.24),
    ]

    tax = 0
    prev = 0
    for limit, rate in brackets:
        if taxable_income > limit:
            tax += (limit - prev) * rate
            prev = limit
        else:
            tax += (taxable_income - prev) * rate
            break

    return {
        "agi": income,
        "taxable_income": taxable_income,
        "tax_liability": round(tax, 2),
        "refund": 0  # placeholder
    }
