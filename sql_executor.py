import pandas as pd
from database import engine


def execute_sql(sql):

    try:
        df = pd.read_sql(sql, engine)

        return {
            "success": True,
            "data": df,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


if __name__ == "__main__":

    sql = """
    SELECT
        c.segment,
        SUM(o.revenue) AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.segment
    ORDER BY total_revenue DESC;
    """

    result = execute_sql(sql)

    if result["success"]:
        print(result["data"])
    else:
        print("SQL Error:")
        print(result["error"])