import pandas as pd
import re


def apply_filters(df: pd.DataFrame, rules: list, logic: str = "AND") -> pd.DataFrame:
    """
    Apply a list of filter rules to a DataFrame.

    Each rule is a dict:
      {
        "column":     str,           # original column name
        "operator":   str,           # see OPERATORS below
        "value":      any,           # scalar or [lo, hi] for between
        "norm_col":   str | None,    # normalized column for numeric ops
      }

    logic: "AND" (all rules must match) or "OR" (any rule matches)

    Supported operators:
      equals, not_equals,
      in, not_in,
      contains, not_contains,
      starts_with, ends_with,
      between, gte, lte, gt, lt,
      is_empty, is_not_empty
    """
    if not rules:
        return df

    masks = []
    for rule in rules:
        col      = rule.get("column", "")
        op       = rule.get("operator", "")
        val      = rule.get("value")
        norm_col = rule.get("norm_col")

        if col not in df.columns:
            continue

        series     = df[col]
        str_series = series.astype(str).str.strip()
        str_lower  = str_series.str.lower()

        # Resolve numeric series
        num_series = None
        if norm_col and norm_col in df.columns:
            num_series = pd.to_numeric(df[norm_col], errors="coerce")
        else:
            num_series = pd.to_numeric(series, errors="coerce")

        mask = pd.Series([True] * len(df), index=df.index)

        if op == "equals":
            mask = str_lower == str(val).lower().strip()

        elif op == "not_equals":
            mask = str_lower != str(val).lower().strip()

        elif op == "in":
            if isinstance(val, list) and val:
                vals_lower = [str(v).lower().strip() for v in val]
                mask = str_lower.isin(vals_lower)
            else:
                mask = pd.Series([True] * len(df), index=df.index)

        elif op == "not_in":
            if isinstance(val, list) and val:
                vals_lower = [str(v).lower().strip() for v in val]
                mask = ~str_lower.isin(vals_lower)

        elif op == "contains":
            mask = str_lower.str.contains(re.escape(str(val).lower()), na=False)

        elif op == "not_contains":
            mask = ~str_lower.str.contains(re.escape(str(val).lower()), na=False)

        elif op == "starts_with":
            mask = str_lower.str.startswith(str(val).lower(), na=False)

        elif op == "ends_with":
            mask = str_lower.str.endswith(str(val).lower(), na=False)

        elif op == "between":
            if isinstance(val, (list, tuple)) and len(val) == 2:
                lo, hi = float(val[0]), float(val[1])
                mask = num_series.between(lo, hi, inclusive="both")
                mask = mask.fillna(False)

        elif op == "gte":
            mask = num_series >= float(val)
            mask = mask.fillna(False)

        elif op == "lte":
            mask = num_series <= float(val)
            mask = mask.fillna(False)

        elif op == "gt":
            mask = num_series > float(val)
            mask = mask.fillna(False)

        elif op == "lt":
            mask = num_series < float(val)
            mask = mask.fillna(False)

        elif op == "is_empty":
            mask = series.isna() | (str_series == "") | (str_lower == "nan")

        elif op == "is_not_empty":
            mask = ~(series.isna() | (str_series == "") | (str_lower == "nan"))

        masks.append(mask)

    if not masks:
        return df

    if logic == "OR":
        final = masks[0]
        for m in masks[1:]:
            final = final | m
    else:  # AND
        final = masks[0]
        for m in masks[1:]:
            final = final & m

    return df[final].copy()
