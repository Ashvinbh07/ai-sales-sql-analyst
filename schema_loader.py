from sqlalchemy import inspect, text

from database import engine


def get_database_schema():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    schema = []

    for table in tables:

        columns = inspector.get_columns(table)

        schema.append(f"{table}(")

        for column in columns:

            column_name = column["name"]
            data_type = str(column["type"])

            schema.append(
                f"    {column_name} {data_type},"
            )

        schema.append(")")
        schema.append("")

    return "\n".join(schema)


def get_date_range():

    query = text("""
        SELECT
            MIN(order_date) AS first_date,
            MAX(order_date) AS last_date
        FROM orders;
    """)

    with engine.connect() as connection:

        result = connection.execute(query).fetchone()

    return result.first_date, result.last_date


if __name__ == "__main__":

    print("Database Schema:")
    print(get_database_schema())

    first_date, last_date = get_date_range()

    print("Database Date Range:")
    print(first_date)
    print(last_date)