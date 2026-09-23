import streamlit as st
import pandas as pd

from sql_generator import generate_sql
from sql_validator import validate_sql
from sql_executor import execute_sql
from sql_corrector import correct_sql
from result_analyzer import analyze_result


def clean_sql(sql):

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


def create_chart(df):

    if df.empty or len(df.columns) < 2:

        st.info(
            "No suitable chart could be generated for this result."
        )

        return

    columns = list(df.columns)

    # --------------------------------
    # Detect numeric columns
    # --------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # --------------------------------
    # Q1 vs Q2 comparison
    # --------------------------------

    q1_columns = [
        col
        for col in columns
        if "q1" in col.lower()
    ]

    q2_columns = [
        col
        for col in columns
        if "q2" in col.lower()
    ]

    if q1_columns and q2_columns:

        category_columns = [
            col
            for col in columns
            if col not in q1_columns
            and col not in q2_columns
        ]

        if category_columns:

            category = category_columns[0]

            chart_data = df[
                [
                    category,
                    q1_columns[0],
                    q2_columns[0]
                ]
            ].copy()

            chart_data = chart_data.set_index(
                category
            )

            st.bar_chart(
                chart_data,
                stack=False
            )

            return

    # --------------------------------
    # Detect month columns
    # --------------------------------

    month_columns = [
        col
        for col in columns
        if col.lower() in [
            "month",
            "order_month"
        ]
    ]

    # --------------------------------
    # Monthly trend
    # --------------------------------

    if month_columns and numeric_columns:

        month_col = month_columns[0]

        metric_columns = [
            col
            for col in numeric_columns
            if col != month_col
        ]

        if metric_columns:

            metric = metric_columns[0]

            chart_data = df[
                [
                    month_col,
                    metric
                ]
            ].copy()

            chart_data = chart_data.sort_values(
                month_col
            )

            chart_data = chart_data.set_index(
                month_col
            )

            st.line_chart(
                chart_data
            )

            return

    # --------------------------------
    # Detect year columns
    # --------------------------------

    year_columns = [
        col
        for col in columns
        if col.lower() in [
            "year",
            "order_year"
        ]
    ]

    # --------------------------------
    # Yearly trend
    # --------------------------------

    if year_columns and numeric_columns:

        year_col = year_columns[0]

        metric_columns = [
            col
            for col in numeric_columns
            if col != year_col
        ]

        if metric_columns:

            metric = metric_columns[0]

            chart_data = df[
                [
                    year_col,
                    metric
                ]
            ].copy()

            chart_data = chart_data.sort_values(
                year_col
            )

            chart_data = chart_data.set_index(
                year_col
            )

            st.line_chart(
                chart_data
            )

            return

    # --------------------------------
    # Category / Segment / City / Product / Customer
    # --------------------------------

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if categorical_columns and numeric_columns:

        category = categorical_columns[0]

        # Ignore numeric ID columns when selecting
        # the metric for visualization.
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

        if metric_columns:

            metric = metric_columns[0]

            chart_data = df[
                [
                    category,
                    metric
                ]
            ].copy()

            chart_data = chart_data.set_index(
                category
            )

            st.bar_chart(
                chart_data
            )

            return

    # --------------------------------
    # No suitable chart
    # --------------------------------

    st.info(
        "No suitable chart could be generated for this result."
    )


def run_analysis(question):

    sql = generate_sql(question)

    sql = clean_sql(sql)

    valid, message = validate_sql(sql)

    if not valid:

        return {
            "success": False,
            "error": message
        }

    result = execute_sql(sql)

    if not result["success"]:

        corrected_sql = correct_sql(
            sql,
            result["error"],
            question
        )

        corrected_sql = clean_sql(
            corrected_sql
        )

        valid, message = validate_sql(
            corrected_sql
        )

        if not valid:

            return {
                "success": False,
                "error": message,
                "sql": sql
            }

        result = execute_sql(
            corrected_sql
        )

        if not result["success"]:

            return {
                "success": False,
                "error": result["error"],
                "sql": corrected_sql
            }

        sql = corrected_sql

    df = result["data"]

    analysis = analyze_result(
        df,
        question
    )

    return {
        "success": True,
        "sql": sql,
        "data": analysis["data"],
        "insight": analysis["insight"]
    }


# --------------------------------
# Streamlit UI
# --------------------------------

st.set_page_config(
    page_title="AI Sales SQL Analyst",
    page_icon="📊",
    layout="wide"
)


st.title(
    "📊 AI Sales SQL Analyst"
)

st.write(
    "Ask a sales business question in natural language "
    "and let AI generate, validate, execute and analyze SQL."
)


question = st.text_input(
    "Ask a business question",
    placeholder=(
        "Example: Which product categories generated "
        "the highest revenue?"
    )
)


if st.button("Analyze"):

    if not question.strip():

        st.warning(
            "Please enter a business question."
        )

    else:

        with st.spinner(
            "Analyzing your question..."
        ):

            result = run_analysis(
                question
            )

        if not result["success"]:

            st.error(
                result["error"]
            )

        else:

            st.success(
                "Analysis completed successfully."
            )

            st.subheader(
                "Generated SQL"
            )

            st.code(
                result["sql"],
                language="sql"
            )

            st.subheader(
                "Query Result"
            )

            st.dataframe(
                result["data"],
                use_container_width=True
            )

            st.subheader(
                "Visualization"
            )

            create_chart(
                result["data"]
            )

            st.subheader(
                "Business Insight"
            )

            st.write(
                result["insight"]
            )