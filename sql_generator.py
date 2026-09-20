import requests
from schema_loader import get_database_schema, get_date_range
from sql_rules import SQL_RULES


def generate_sql(question):

    schema = get_database_schema()

    first_date, last_date = get_date_range()

    prompt = f"""
{SQL_RULES}

DATABASE SCHEMA:
{schema}

DATABASE DATE RANGE:
{first_date} to {last_date}

USER QUESTION:
{question}

TASK:

Generate PostgreSQL SQL that directly answers the user's question.

IMPORTANT:

- Understand the exact business intent.
- Preserve the requested metric and aggregation level.
- Include required comparisons and time periods.
- Return ONLY SQL.
- Do not use markdown.
- Do not explain.

Before returning SQL, internally verify:

1. Every table exists.
2. Every column exists.
3. JOIN conditions are correct.
4. The requested metric is calculated correctly.
5. The aggregation level is correct.
6. Required date filters are included only when requested.
7. Required comparisons are included.
8. No columns or tables have been invented.
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

    question = input("Ask a question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)