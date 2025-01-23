import pandas as pd
from faker import Faker
import random

fake = Faker()
num_records = 1000

data = {
    "InvoiceID": [fake.uuid4()[:8] for _ in range(num_records)],
    "Date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_records)],
    "CustomerName": [fake.name() for _ in range(num_records)],
    "CustomerID": [fake.uuid4()[:6] for _ in range(num_records)],
    "Product": [random.choice(["Laptop", "Phone", "Tablet", "Headphones", "Monitor"]) for _ in range(num_records)],
    "Quantity": [random.randint(1, 10) for _ in range(num_records)],
    "UnitPrice": [random.randint(50, 1500) for _ in range(num_records)],
    "Tax": [random.uniform(0.05, 0.2) for _ in range(num_records)],
    "PaymentMethod": [random.choice(["Cash", "Credit Card", "Bank Transfer", "PayPal"]) for _ in range(num_records)],
    "Status": [random.choice(["Paid", "Pending", "Overdue"]) for _ in range(num_records)],
}

df = pd.DataFrame(data)
df["Total"] = (df["Quantity"] * df["UnitPrice"]) * (1 + df["Tax"])
df.to_csv("data/invoices_dataset.csv", index=False)
print("Dataset created!")
