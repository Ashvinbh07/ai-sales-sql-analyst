import re
import requests

from schema_loader import get_database_schema, get_date_range
from sql_rules import SQL_RULES


def clean_sql(sql):

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


def repair_known_schema_errors(sql, error):

    error_lower = error.lower()

    # --------------------------------
    # Customer segment
    # --------------------------------

    if 'column "segment" does not exist' in error_lower:

        sql = re.sub(
            r"SELECT\s+segment\s*,",
            "SELECT c.segment,",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"GROUP BY\s+segment",
            "GROUP BY c.segment",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"FROM orders",
            """FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id""",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"\bSUM\(revenue\)",
            "SUM(o.revenue)",
            sql,
            flags=re.IGNORECASE
        )

        sql = re.sub(
            r"\border_date\b",
            "o.order_date",
            sql,
            flags=re.IGNORECASE
        )

        return sql

    return sql


def correct_sql(sql, error, question):

    schema = get_database_schema()

    first_date, last_date = get_date_range()

    prompt = f"""
You are an expert PostgreSQL SQL debugger for a sales analytics system.

Fix the broken SQL while preserving the EXACT business intent.

DATABASE SCHEMA:
{schema}

DATABASE DATE RANGE:
{first_date} to {last_date}

USER QUESTION:
{question}

BROKEN SQL:
{sql}

DATABASE ERROR:
{error}

SQL RULES:
{SQL_RULES}

IMPORTANT TABLE RELATIONSHIPS:

orders.customer_id = customers.customer_id

orders.product_id = products.product_id

COLUMN OWNERSHIP:

customers:
customer_id
customer_name
segment
city
signup_date

orders:
order_id
customer_id
product_id
order_date
quantity
revenue
profit

products:
product_id
product_name
category
price

IMPORTANT:

If the question requires customers.segment, you MUST join customers:

FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id

Then use:

c.segment

If the question requires products.category, you MUST join products:

FROM orders o
JOIN products p
    ON o.product_id = p.product_id

Then use:

p.category

Do not use customer columns directly from orders.

Do not use product columns directly from orders.

Always use table aliases.

Preserve all required calculations, comparisons,
grouping, ranking and time periods.

DATE RULES:

- Do not add a date filter unless the user specifies a date,
  year, month, quarter or time period.
- If a year is specified, filter for that year.
- If a date range is specified, use that range.
- Q1 means January through March.
- Q2 means April through June.
- Q3 means July through September.
- Q4 means October through December.
- Do not assume a year that the user did not specify.

OUTPUT RULES:

- Return ONLY SQL.
- Only SELECT or WITH queries.
- No markdown.
- No explanation.
- Do not invent columns.
- Do not invent tables.

Before returning SQL, verify:

1. Every table exists.
2. Every column exists.
3. Every column belongs to the correct table.
4. Required JOINs exist.
5. JOIN conditions are correct.
6. The original question is preserved.
7. Required comparisons are preserved.
8. Required calculations are preserved.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        }
    )

    response.raise_for_status()

    corrected_sql = response.json()["response"].strip()

    corrected_sql = clean_sql(corrected_sql)

    # --------------------------------
    # Programmatic schema repair
    # --------------------------------

    corrected_sql = repair_known_schema_errors(
        corrected_sql,
        error
    )

    return corrected_sql


if __name__ == "__main__":

    bad_sql = """
    WITH Q1_Revenue AS (
        SELECT
            segment,
            SUM(revenue) AS Q1_Revenue
        FROM orders
        WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
        GROUP BY segment
    ),
    Q2_Revenue AS (
        SELECT
            segment,
            SUM(revenue) AS Q2_Revenue
        FROM orders
        WHERE order_date BETWEEN '2024-04-01' AND '2024-06-30'
        GROUP BY segment
    )
    SELECT *
    FROM Q1_Revenue
    JOIN Q2_Revenue
        ON Q1_Revenue.segment = Q2_Revenue.segment;
    """

    error = 'column "segment" does not exist'

    question = (
        "Which customer segments had the largest "
        "revenue decline in Q2 compared with Q1?"
    )

    corrected = correct_sql(
        bad_sql,
        error,
        question
    )

    print("\nCorrected SQL:")
    print(corrected)