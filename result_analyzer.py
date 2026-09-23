import requests
import pandas as pd


def get_verified_facts(df, question):

    facts = []

    if df.empty:
        return facts

    columns = list(df.columns)

    # --------------------------------
    # Find likely metric columns
    # --------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Ignore ID columns
    metric_columns = [
        col
        for col in numeric_columns
        if not col.lower().endswith("_id")
        and col.lower() not in [
            "id",
            "customer_id",
            "product_id",
            "order_id"
        ]
    ]

    if not metric_columns:
        return facts

    # Prefer revenue metric when available
    revenue_columns = [
        col
        for col in metric_columns
        if "revenue" in col.lower()
    ]

    if revenue_columns:
        metric = revenue_columns[0]
    else:
        metric = metric_columns[0]

    # --------------------------------
    # Find likely dimension column
    # --------------------------------

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    dimension = None

    if categorical_columns:
        dimension = categorical_columns[0]

    # --------------------------------
    # Time-series detection
    # --------------------------------

    time_columns = [
        col
        for col in columns
        if col.lower() in [
            "month",
            "order_month",
            "year",
            "order_year"
        ]
    ]

    if time_columns:
        dimension = time_columns[0]

    # --------------------------------
    # Calculate verified maximum
    # --------------------------------

    if dimension:

        max_row = df.loc[
            df[metric].idxmax()
        ]

        min_row = df.loc[
            df[metric].idxmin()
        ]

        max_value = max_row[metric]
        min_value = min_row[metric]

        max_dimension = max_row[dimension]
        min_dimension = min_row[dimension]

        facts.append(
            f"Verified highest {metric}: "
            f"{max_dimension} = {max_value}"
        )

        facts.append(
            f"Verified lowest {metric}: "
            f"{min_dimension} = {min_value}"
        )

    # --------------------------------
    # Top row
    # --------------------------------

    sorted_df = df.sort_values(
        by=metric,
        ascending=False
    )

    top_row = sorted_df.iloc[0]

    if dimension:

        facts.append(
            f"Verified top {dimension}: "
            f"{top_row[dimension]} = {top_row[metric]}"
        )

    return facts


def analyze_result(df, question):

    if df.empty:

        return {
            "data": df,
            "insight": "No data was returned for this question."
        }

    result_text = df.to_string(index=False)

    verified_facts = get_verified_facts(
        df,
        question
    )

    verified_text = "\n".join(
        verified_facts
    )

    prompt = f"""
You are a business analyst specializing in sales analytics.

USER QUESTION:
{question}

QUERY RESULT:
{result_text}

VERIFIED FACTS CALCULATED DIRECTLY FROM THE QUERY RESULT:
{verified_text}

TASK:

Provide a concise business insight answering the user's original question.

IMPORTANT:

- Use the QUERY RESULT as the source of truth.
- Use the VERIFIED FACTS as authoritative calculations.
- Do not calculate maximum or minimum values yourself.
- Do not override or contradict the VERIFIED FACTS.
- Do not use information from a visualization.
- Do not invent numbers.
- Do not invent facts.
- Do not invent percentages.
- Do not add metrics that are not present in the query result.
- Do not add currency symbols.
- Use the exact values provided by the verified facts when mentioning highest or lowest values.
- Keep the answer concise.
- Use simple business language.
- Return only the final business insight.
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

    insight = response.json()["response"].strip()

    insight = (
        insight
        .replace("$", "")
        .replace("₹", "")
        .replace("€", "")
        .replace("£", "")
    )

    return {
        "data": df,
        "insight": insight
    }


if __name__ == "__main__":

    test_data = pd.DataFrame({
        "month": [
            1, 2, 3, 4, 5, 6,
            7, 8, 9, 10, 11, 12
        ],
        "revenue": [
            1301504.07,
            1293164.07,
            1334110.04,
            1175761.21,
            1379739.44,
            1244841.65,
            1254930.68,
            1311546.29,
            1338245.97,
            1278446.78,
            1150142.99,
            1282526.39
        ]
    })

    question = (
        "What was the monthly revenue trend in 2024?"
    )

    result = analyze_result(
        test_data,
        question
    )

    print("\nBusiness Insight:")
    print(result["insight"])