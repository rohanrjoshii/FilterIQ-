"""
Simple query parser for natural language-like filter queries.
Converts queries like "Gender is Female AND Age > 25" into structured rules.
"""
import re
from typing import List, Dict, Any


def parse_query(query: str, columns: List[str]) -> tuple[List[Dict[str, Any]], str]:
    """
    Parse a natural language query into structured filter rules.
    
    Returns: (rules, logic)
    - rules: list of filter rule dicts
    - logic: "AND" or "OR"
    
    Examples:
        "Gender is Female" → [{"column": "Gender", "operator": "equals", "value": "Female"}], "AND"
        "Age > 25 AND City contains Mumbai" → [...], "AND"
    """
    query = query.strip()
    if not query:
        return [], "AND"
    
    # Detect primary logic (AND vs OR)
    # Count AND vs OR occurrences (case insensitive)
    and_count = len(re.findall(r'\band\b', query, re.IGNORECASE))
    or_count = len(re.findall(r'\bor\b', query, re.IGNORECASE))
    primary_logic = "OR" if or_count > and_count else "AND"
    
    # Split by the primary logic operator
    if primary_logic == "OR":
        parts = re.split(r'\s+or\s+', query, flags=re.IGNORECASE)
    else:
        parts = re.split(r'\s+and\s+', query, flags=re.IGNORECASE)
    
    rules = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        rule = parse_single_condition(part, columns)
        if rule:
            rules.append(rule)
    
    return rules, primary_logic


def parse_single_condition(expr: str, columns: List[str]) -> Dict[str, Any] | None:
    """
    Parse a single condition like "Age > 25" or "Gender is Female".
    
    Supported patterns:
    - Column is Value
    - Column = Value
    - Column contains Value
    - Column > Value
    - Column < Value
    - Column >= Value
    - Column <= Value
    - Column between X and Y
    - Column starts with Value
    - Column ends with Value
    """
    expr = expr.strip()
    
    # Find the column name (fuzzy match)
    col = None
    col_pattern = None
    
    # Try exact match first
    for c in columns:
        if expr.lower().startswith(c.lower()):
            col = c
            col_pattern = c
            break
    
    # Try fuzzy match (remove spaces, special chars)
    if not col:
        for c in columns:
            c_clean = re.sub(r'[^a-z0-9]', '', c.lower())
            expr_start = re.sub(r'[^a-z0-9]', '', expr.lower()[:len(c)+5])
            if expr_start.startswith(c_clean):
                col = c
                col_pattern = c
                break
    
    if not col:
        return None
    
    # Remove column name from expression
    remainder = expr[len(col_pattern):].strip()
    
    # Parse operator and value
    # Between pattern
    m = re.match(r'between\s+(.+?)\s+and\s+(.+)', remainder, re.IGNORECASE)
    if m:
        return {
            "column": col,
            "operator": "between",
            "value": [m.group(1).strip(), m.group(2).strip()],
            "norm_col": find_norm_col(col, columns)
        }
    
    # Comparison operators
    operators = [
        (r'is\s+not\s+(.+)', 'not_equals'),
        (r'is\s+(.+)', 'equals'),
        (r'=\s*(.+)', 'equals'),
        (r'!=\s*(.+)', 'not_equals'),
        (r'contains\s+(.+)', 'contains'),
        (r'not\s+contains\s+(.+)', 'not_contains'),
        (r'starts\s+with\s+(.+)', 'starts_with'),
        (r'ends\s+with\s+(.+)', 'ends_with'),
        (r'>=\s*(.+)', 'gte'),
        (r'<=\s*(.+)', 'lte'),
        (r'>\s*(.+)', 'gt'),
        (r'<\s*(.+)', 'lt'),
    ]
    
    for pattern, op in operators:
        m = re.match(pattern, remainder, re.IGNORECASE)
        if m:
            value = m.group(1).strip().strip('"').strip("'")
            rule = {
                "column": col,
                "operator": op,
                "value": value
            }
            # Add norm_col for numeric operations
            if op in ('between', 'gte', 'lte', 'gt', 'lt'):
                norm_col = find_norm_col(col, columns)
                if norm_col:
                    rule["norm_col"] = norm_col
            return rule
    
    return None


def find_norm_col(col: str, all_columns: List[str]) -> str | None:
    """Find the normalized column for a given column."""
    # Look for _norm_{col}_* patterns
    col_lower = col.lower().replace(" ", "").replace("_", "").replace("-", "")
    for c in all_columns:
        if c.startswith("_norm_"):
            c_clean = c.replace("_norm_", "").replace("_cm", "").replace("_num", "").replace("_salary", "").replace("_text", "")
            c_clean = c_clean.lower().replace(" ", "").replace("_", "").replace("-", "")
            if c_clean == col_lower:
                return c
    return None
