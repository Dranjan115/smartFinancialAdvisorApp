import requests

# Replace with actual feature inputs in the order model expects
payload = {
    "age": 35,
    "monthly_income": 25000,
    "education":1,
    "work_experience": 5,
    "family_size": 4,
    "credit_card_spend": 3000,
    "mortgage_amount": 50000,
    "has_existing_loan": 1,
    "has_cd_account": 0,
    "uses_online_banking": 1,
    "has_bank_credit_card": 0
}

try:
    response = requests.post("http://127.0.0.1:5000/predict", json=payload)

    if response.status_code == 200:
        print("✅ Server response:", response.json())
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print("❌ Request failed:", e)
