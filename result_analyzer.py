import requests
import pandas as pd


def analyze_result(df, question):

    if df.empty:

        return {
            "data": df,
            "insight": "No data was returned for this question."
        }

    result_text = df.to_string(index=False)

    prompt = f"""
You are a business analyst specializing in sales analytics.

USER QUESTION:
{question}

QUERY RESULT:
{result_text}

TASK:

Analyze the query result and provide a concise business insight.

STRICT RULES:

- Answer the user's original question directly.
- Use ONLY information present in the query result.
- Do not invent numbers, facts, or business information.
- Do not assume information that is not present.
- Do not invent a currency symbol.
- Display monetary values as plain numbers.
- Mention important values when useful.
- If the result contains a comparison, describe the comparison using the available values.
- If the result contains a growth or decline percentage column, you may mention that percentage.
- If the result DOES NOT contain a growth or decline percentage column, DO NOT calculate or invent a percentage.
- Do not calculate new percentages from raw values.
- Do not calculate new metrics that are not present in the query result.
- For time-series results, describe the visible trend using the available values.
- Identify the most important finding.
- Keep the insight concise.
- Use simple business language.
- Do not provide SQL.
- Do not explain your reasoning.
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

    # Remove currency symbols because this project
    # does not specify a currency.
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
        "category": [
            "Furniture",
            "Electronics",
            "Books",
            "Clothing",
            "Home"
        ],
        "total_revenue": [
            8636868.26,
            7375911.73,
            7140756.55,
            4379188.44,
            2935717.02
        ]
    })

    question = (
        "Which product categories generated "
        "the highest revenue?"
    )

    result = analyze_result(
        test_data,
        question
    )

    print("\nBusiness Insight:")
    print(result["insight"])