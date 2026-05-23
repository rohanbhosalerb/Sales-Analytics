"""
Script to generate sample sales data for analysis.
Run this first to create the dataset.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Clothing", "Groceries", "Furniture", "Sports"]
PRODUCTS = {
    "Electronics": ["Laptop", "Phone", "Tablet", "Headphones", "Monitor"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes"],
    "Groceries": ["Rice", "Pasta", "Olive Oil", "Coffee", "Cereal"],
    "Furniture": ["Chair", "Desk", "Sofa", "Bookshelf", "Lamp"],
    "Sports": ["Yoga Mat", "Dumbbells", "Cycling Helmet", "Tennis Racket", "Running Shoes"],
}
PRICE_RANGE = {
    "Electronics": (200, 1500),
    "Clothing": (20, 200),
    "Groceries": (5, 50),
    "Furniture": (100, 800),
    "Sports": (30, 300),
}

n = 1000
dates = pd.date_range(start="2023-01-01", end="2023-12-31", periods=n)
categories = np.random.choice(CATEGORIES, n)
products = [np.random.choice(PRODUCTS[c]) for c in categories]
prices = [round(np.random.uniform(*PRICE_RANGE[c]), 2) for c in categories]
quantities = np.random.randint(1, 10, n)
regions = np.random.choice(REGIONS, n)
discounts = np.round(np.random.choice([0, 0.05, 0.10, 0.15, 0.20], n), 2)

df = pd.DataFrame({
    "order_id": [f"ORD-{1000 + i}" for i in range(n)],
    "date": dates,
    "region": regions,
    "category": categories,
    "product": products,
    "unit_price": prices,
    "quantity": quantities,
    "discount": discounts,
})

df["revenue"] = (df["unit_price"] * df["quantity"] * (1 - df["discount"])).round(2)

# Inject some missing values to make analysis realistic
for col in ["unit_price", "quantity", "discount"]:
    idx = np.random.choice(df.index, size=20, replace=False)
    df.loc[idx, col] = np.nan

os.makedirs("data", exist_ok=True)
df.to_csv("data/sales_data.csv", index=False)
print(f"✅ Dataset created: data/sales_data.csv ({len(df)} rows)")
