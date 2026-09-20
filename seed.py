import random
from datetime import date, timedelta

import pandas as pd
from sqlalchemy import text

from database import engine


# -------------------------
# 1. Customers
# -------------------------

segments = ["Consumer", "Corporate", "Small Business"]
cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad"]

customers = []

for i in range(1, 1001):
    customers.append({
        "customer_id": i,
        "customer_name": f"Customer {i}",
        "segment": random.choice(segments),
        "city": random.choice(cities),
        "signup_date": date(2024, 1, 1) +
                       timedelta(days=random.randint(0, 730))
    })

customers_df = pd.DataFrame(customers)


# -------------------------
# 2. Products
# -------------------------

categories = ["Electronics", "Furniture", "Clothing", "Books", "Home"]

products = []

for i in range(1, 51):
    products.append({
        "product_id": i,
        "product_name": f"Product {i}",
        "category": random.choice(categories),
        "price": round(random.uniform(10, 1000), 2)
    })

products_df = pd.DataFrame(products)


# -------------------------
# 3. Orders
# -------------------------

orders = []

for i in range(1, 20001):

    quantity = random.randint(1, 5)
    price = random.uniform(10, 1000)

    revenue = quantity * price
    profit = revenue * random.uniform(0.05, 0.30)

    orders.append({
        "order_id": i,
        "customer_id": random.randint(1, 1000),
        "product_id": random.randint(1, 50),
        "order_date": date(2024, 1, 1) +
                      timedelta(days=random.randint(0, 730)),
        "quantity": quantity,
        "revenue": round(revenue, 2),
        "profit": round(profit, 2)
    })

orders_df = pd.DataFrame(orders)


# -------------------------
# 4. Insert into PostgreSQL
# -------------------------

customers_df.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False
)

products_df.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

orders_df.to_sql(
    "orders",
    engine,
    if_exists="append",
    index=False
)

print("Data inserted successfully!")
print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Orders: {len(orders_df)}")