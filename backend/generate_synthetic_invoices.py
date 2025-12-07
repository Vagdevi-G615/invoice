# generate_synthetic_invoices.py
"""
Generate a small synthetic invoice-like dataset (CSV) with text and label columns.
Labels: 'accounts_payable', 'expense', 'purchase_order', 'tax', 'other'
"""

import csv
import random
from faker import Faker
import os

fake = Faker()

OUTPUT_CSV = "data/synthetic_invoices.csv"
NUM_SAMPLES = 1200  # small but enough to run quick experiments

LABELS = [
    ("accounts_payable", [
        "Invoice from {vendor} for invoice #{inv} total {amt} due on {date}. Please remit payment.",
        "Payment request - Invoice {inv}; Amount: {amt}. For Accounts Payable processing."
    ]),
    ("expense", [
        "Expense reimbursement claim by {employee} for {amt} on {date}. Category: travel.",
        "Reimbursement: taxi {amt}, lunch {amt2}. Employee: {employee}."
    ]),
    ("purchase_order", [
        "PO #{po} confirmation: items {items}. Total {amt}. Ship to {address}.",
        "Purchase Order {po} received for vendor {vendor}. Qty: {qty}. Total: {amt}."
    ]),
    ("tax", [
        "Tax invoice {inv}: GST {gst}% on amount {amt}. Taxable value {taxable}.",
        "TAX INVOICE - Invoice No: {inv}. IGST {igst} applied. Total {amt}."
    ]),
    ("other", [
        "Credit note {cn} issued to {vendor} for amount {amt}.",
        "Misc document: reference {ref}. Notes: {note}"
    ])
]

os.makedirs("data", exist_ok=True)

def rand_amount():
    return f"₹{random.randint(100, 200000)}.00"

def generate_text(template):
    return template.format(
        vendor=fake.company(),
        inv=random.randint(1000, 99999),
        amt=rand_amount(),
        amt2=rand_amount(),
        date=fake.date_between(start_date='-365d', end_date='today').isoformat(),
        employee=fake.name(),
        po=random.randint(10000,99999),
        items="; ".join([fake.word() for _ in range(random.randint(1,4))]),
        address=fake.address().replace("\n", ", "),
        qty=random.randint(1,100),
        gst=random.choice([5,12,18]),
        taxable=f"₹{random.randint(100,100000)}",
        igst=random.choice([0,5,12,18]),
        cn=random.randint(100,9999),
        ref=random.randint(100000,999999),
        note=fake.sentence(nb_words=6)
    )

rows = []
for _ in range(NUM_SAMPLES):
    label, templates = random.choice(LABELS)
    template = random.choice(templates)
    text = generate_text(template)
    # Add some noise / random lines to simulate messy OCR
    if random.random() < 0.25:
        text += " " + fake.sentence(nb_words=random.randint(3,8))
    rows.append((text, label))

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(rows)

print(f"Generated {NUM_SAMPLES} synthetic invoices -> {OUTPUT_CSV}")
