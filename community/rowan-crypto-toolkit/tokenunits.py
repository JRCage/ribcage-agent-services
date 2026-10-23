"""TokenUnits: exact decimal/raw token conversions. Offline; no token metadata lookup."""
import argparse
from decimal import Decimal, InvalidOperation, localcontext

def check_decimals(decimals):
    if type(decimals) is not int or not 0 <= decimals <= 30:
        raise ValueError("decimals must be integer 0..30")

def to_raw(amount, decimals):
    check_decimals(decimals)
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid amount") from exc
    if not value.is_finite() or value < 0:
        raise ValueError("amount must be finite and nonnegative")
    raw = value * (10 ** decimals)
    if raw != raw.to_integral_value():
        raise ValueError("amount exceeds token precision")
    return int(raw)

def from_raw(raw, decimals):
    check_decimals(decimals)
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
        raise ValueError("raw must be nonnegative integer")
    with localcontext() as ctx:
        ctx.prec = max(50, len(str(raw)) + decimals + 2)
        return format(Decimal(raw) / (10 ** decimals), 'f')

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=["to-raw", "from-raw"])
    p.add_argument("amount")
    p.add_argument("--decimals", type=int, required=True)
    a = p.parse_args()
    if a.mode == "to-raw":
        print(to_raw(a.amount, a.decimals))
    else:
        if not a.amount.isascii() or not a.amount.isdecimal():
            p.error("raw must contain only ASCII digits")
        print(from_raw(int(a.amount), a.decimals))
