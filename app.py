import streamlit as st

from sql_generator import generate_sql
from sql_validator import validate_sql
from sql_executor import execute_sql
from sql_corrector import correct_sql
from result_analyzer import analyze_result


def clean_sql(sql):
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    return sql.strip()


def run_analysis(question):

    # Generate SQL
    sql = generate_sql(question)
    sql = clean_sql(sql)

    # Validate SQL
    valid, message = validate_sql(sql)

    if not valid:
        return {
            "success": False,
            "error": message
        }

    # Execute SQL
    result = execute_sql(sql)

    # Automatic correction
    if not result["success"]:

        corrected_sql = correct_sql(
            sql,
            result["error"],
            question
        )

        corrected_sql = clean_sql(corrected_sql)

        # Validate corrected SQL
        valid, message = validate_sql(corrected_sql)

        if not valid:
            return {
                "success": False,
                "error": message,
                "sql": sql
            }

        # Execute corrected SQL
        result = execute_sql(corrected_sql)

        if not result["success"]:
            return {
                "success": False,
                "error": result["error"],
                "sql": corrected_sql
            }

        sql = corrected_sql

    # Analyze result
    df = result["data"]

    analyzed_df = analyze_result(df)

    return {
        "success": True,
        "sql": sql,
        "data": analyzed_df
    }


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="AI SQL Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI SQL Analyst")

st.write(
    "Ask a business question in natural language "
    "and let AI generate, validate and execute SQL."
)

question = st.text_input(
    "Ask a business question",
    placeholder=(
        "Example: Which customer segments had the largest "
        "revenue decline in Q2 compared with Q1?"
    )
)


if st.button("Analyze"):

    if not question.strip():

        st.warning("Please enter a business question.")

    else:

        with st.spinner("Analyzing your question..."):

            result = run_analysis(question)

        if not result["success"]:

            st.error(result["error"])

        else:

            st.success("Analysis completed successfully.")

            # -----------------------------
            # Generated SQL
            # -----------------------------

            st.subheader("Generated SQL")

            st.code(
                result["sql"],
                language="sql"
            )

            # -----------------------------
            # Query Result
            # -----------------------------

            st.subheader("Query Result")

            st.dataframe(
                result["data"],
                use_container_width=True
            )

            # -----------------------------
            # Revenue Comparison Chart
            # -----------------------------

            st.subheader("Revenue Comparison")

            if (
                "segment" in result["data"].columns
                and "total_revenue_q1" in result["data"].columns
                and "total_revenue_q2" in result["data"].columns
            ):

                chart_data = result["data"][
                    [
                        "segment",
                        "total_revenue_q1",
                        "total_revenue_q2"
                    ]
                ].set_index("segment")

                st.bar_chart(chart_data)

            # -----------------------------
            # Business Insight
            # -----------------------------

            st.subheader("Business Insight")

            df = result["data"]

            if (
                "percentage_change" in df.columns
                and "segment" in df.columns
            ):

                largest_decline = df.iloc[0]

                st.write(
                    f"**{largest_decline['segment']}** had the "
                    f"largest revenue decline of "
                    f"**{largest_decline['percentage_change']:.2f}%**."
                )

            else:

                st.write(
                    "The query was executed successfully. "
                    "Review the results above for insights."
                )