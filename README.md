# 🏦 Loan Eligibility Prediction API

This Flask-based API uses a trained machine learning model to predict whether a user is eligible for a personal loan based on financial and personal details.

## 🚀 How to Run

1. Clone the repo
2. Create a virtual environment
3. Install requirements:  
   `pip install -r requirements.txt`
4. Run the API:  
   `python app.py`

## 🧾 Sample Input

```json
{
  "age": 35,
  "experience": 5,
  "income": 10,
  "family": 2,
  "ccavg": 1,
  "education": 2,
  "mortgage": 0,
  "securities_account": 0,
  "cd_account": 0,
  "online": 1,
  "creditcard": 0
}
