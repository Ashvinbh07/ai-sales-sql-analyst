import re


FORBIDDEN_COMMANDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE"
]


def validate_sql(sql):

    sql_upper = sql.upper().strip()

    # Must start with SELECT or WITH
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, "Only SELECT queries are allowed."

    # Check forbidden commands
    for command in FORBIDDEN_COMMANDS:
        pattern = rf"\b{command}\b"

        if re.search(pattern, sql_upper):
            return False, f"Forbidden SQL command: {command}"

    return True, "SQL is valid."


if __name__ == "__main__":

    sql = "DROP TABLE customers;"

    valid, message = validate_sql(sql)

    print(valid)
    print(message)