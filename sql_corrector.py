import requests

from schema_loader import get_database_schema, get_date_range
from sql_rules import SQL_RULES


def correct_sql(sql, error, question):

    schema = get_database_schema()

    first_date, last_date = get_date_range()

    prompt = f"""
{SQL_RULES}

TASK:
Fix the broken SQL query below.

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

CORRECTION REQUIREMENTS:

- Fix the SQL error.
- Preserve the exact business intent.
- Preserve the requested metric.
- Preserve the requested aggregation level.
- Preserve required comparisons and time periods.
- Follow all rules provided above.
- Do not invent tables or columns.
- Return ONLY the corrected SQL.
- Do not use markdown.
- Do not explain.
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

    return response.json()["response"].strip()


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