import re
import pandas as pd


# ---------------------------------------------------------------------------
# Height
# ---------------------------------------------------------------------------

def parse_height_to_cm(val) -> float | None:
    if pd.isna(val):
        return None
    val = str(val).strip().lower()

    # Already cm: "175cm" or "175"
    m = re.match(r"^(\d{2,3})\s*cm$", val)
    if m:
        return float(m.group(1))

    # Pure number — if between 100-250 assume cm, if 4-8 assume feet
    m = re.match(r"^(\d+(?:\.\d+)?)$", val)
    if m:
        n = float(m.group(1))
        if 100 <= n <= 250:
            return n
        if 4 <= n <= 8:
            return round(n * 30.48, 1)
        return None

    # "5ft 8in" / "5'8"" / "5'8" / "5 feet 8 inches"
    m = re.match(r"(\d)\s*(?:ft|feet|'|′)\s*(\d{1,2})\s*(?:in|inch(?:es)?|\")?", val)
    if m:
        return round(int(m.group(1)) * 30.48 + int(m.group(2)) * 2.54, 1)

    # "5ft" / "5'" alone
    m = re.match(r"(\d)\s*(?:ft|feet|'|′)\s*$", val)
    if m:
        return round(int(m.group(1)) * 30.48, 1)

    # "5.8" feet style
    m = re.match(r"(\d)\.(\d{1,2})", val)
    if m:
        ft = int(m.group(1))
        inch = int(m.group(2))
        return round(ft * 30.48 + inch * 2.54, 1)

    return None


# ---------------------------------------------------------------------------
# Salary
# ---------------------------------------------------------------------------

def parse_salary_to_annual_inr(val) -> float | None:
    if pd.isna(val):
        return None
    raw = str(val).strip().lower().replace(",", "")

    # Detect multiplier
    if "crore" in raw or "cr" in raw:
        multiplier = 10_000_000
    elif "lakh" in raw or "lac" in raw or " l" in raw:
        multiplier = 100_000
    elif "k" in raw:
        multiplier = 1_000
    elif "usd" in raw or "$" in raw:
        multiplier = 83_000  # approx annual USD→INR
    elif "per month" in raw or "/month" in raw or "pm" in raw:
        multiplier = 12  # monthly → annual
    else:
        multiplier = 1

    numbers = re.findall(r"\d+(?:\.\d+)?", raw)
    if not numbers:
        return None

    nums = [float(n) for n in numbers[:2]]
    avg = sum(nums) / len(nums)
    return round(avg * multiplier, 0)


# ---------------------------------------------------------------------------
# Age
# ---------------------------------------------------------------------------

def parse_age(val) -> float | None:
    if pd.isna(val):
        return None
    try:
        v = float(str(val).strip())
        if 0 < v < 120:
            return v
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Text normalization
# ---------------------------------------------------------------------------

def normalize_text(val) -> str:
    if pd.isna(val):
        return ""
    return str(val).strip().lower()


# ---------------------------------------------------------------------------
# Apply all normalizations to a DataFrame
# ---------------------------------------------------------------------------

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if col.startswith("_norm_"):
            continue
        cl = col.lower().replace(" ", "").replace("_", "").replace("-", "").replace("/", "")

        if any(h in cl for h in ("height", "hight", "ht")):
            df[f"_norm_{col}_cm"] = df[col].apply(parse_height_to_cm)

        elif any(h in cl for h in ("age", "yrs")):
            df[f"_norm_{col}_num"] = df[col].apply(parse_age)

        elif any(h in cl for h in ("salary", "income", "ctc", "package", "pay", "sal")):
            df[f"_norm_{col}_salary"] = df[col].apply(parse_salary_to_annual_inr)

        elif df[col].dtype == object:
            df[f"_norm_{col}_text"] = df[col].apply(normalize_text)

    return df
