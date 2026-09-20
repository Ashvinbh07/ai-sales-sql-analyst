def analyze_result(df):

    print("\n--- Analysis ---")

    # Detect Q1/Q2 revenue columns
    if (
        "total_revenue_q1" in df.columns
        and "total_revenue_q2" in df.columns
    ):

        df["revenue_change"] = (
            df["total_revenue_q2"]
            - df["total_revenue_q1"]
        )

        df["percentage_change"] = (
            df["revenue_change"]
            / df["total_revenue_q1"]
        ) * 100

        # Sort by percentage decline
        df = df.sort_values(
            "percentage_change"
        )

        print(df)

        largest_decline = df.iloc[0]

        print("\nLargest Revenue Decline:")

        print(
            f"{largest_decline['segment']} "
            f"({largest_decline['percentage_change']:.2f}%)"
        )

        return df

    print("No revenue comparison found.")

    return df