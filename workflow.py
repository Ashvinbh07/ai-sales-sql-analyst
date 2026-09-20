from sql_generator import generate_sql
from sql_validator import validate_sql
from sql_executor import execute_sql
from sql_corrector import correct_sql
from result_analyzer import analyze_result


def clean_sql(sql):
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    return sql.strip()


def run_workflow(question):

    print("\nGenerating SQL...")

    sql = generate_sql(question)
    sql = clean_sql(sql)

    print("\nGenerated SQL:")
    print(sql)

    print("\nValidating SQL...")

    valid, message = validate_sql(sql)

    if not valid:
        print("Validation failed:", message)
        return

    print("SQL is valid.")

    print("\nExecuting SQL...")

    result = execute_sql(sql)

    # Automatic SQL correction
    if not result["success"]:

        print("\nSQL Error:")
        print(result["error"])

        print("\nAttempting automatic SQL correction...")

        corrected_sql = correct_sql(
            sql,
            result["error"],
            question
        )

        corrected_sql = clean_sql(corrected_sql)

        print("\nCorrected SQL:")
        print(corrected_sql)

        print("\nValidating corrected SQL...")

        valid, message = validate_sql(corrected_sql)

        if not valid:
            print("Corrected SQL validation failed:", message)
            return

        print("Corrected SQL is valid.")

        print("\nExecuting corrected SQL...")

        result = execute_sql(corrected_sql)

        if not result["success"]:
            print("\nCorrected SQL still failed:")
            print(result["error"])
            return

        sql = corrected_sql

    # Analyze result
    print("\nResult:")

    df = result["data"]

    print(df)

    print("\nAnalyzing result...")

    analyze_result(df)


if __name__ == "__main__":

    question = input("\nAsk a business question: ")

    run_workflow(question)