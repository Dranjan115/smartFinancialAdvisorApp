from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("loan_model.pkl")

@app.route('/')
def index():
    return render_template('form.html')

# ✅ Android/Java will POST JSON here
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            data = request.get_json()

            features = np.array([
                float(data['age']),
                float(data['experience']),
                float(data['income']),
                float(data['family']),
                float(data['ccavg']),
                float(data['education']),
                float(data['mortgage']),
                float(data['securities_account']),
                float(data['cd_account']),
                float(data['online']),
                float(data['creditcard'])
            ]).reshape(1, -1)

            prediction = model.predict(features)[0]
            confidence = model.predict_proba(features)[0][1] * 100

            return jsonify({
                "approval": bool(prediction),
                "confidence": round(confidence, 2)
            })

        else:
            # ✅ Browser HTML form submission
            data = request.form

            features = np.array([
                float(data['age']),
                float(data['experience']),
                float(data['income']),
                float(data['family']),
                float(data['ccavg']),
                float(data['education']),
                float(data['mortgage']),
                int('securities_account' in data),
                int('cd_account' in data),
                int('online' in data),
                int('creditcard' in data)
            ]).reshape(1, -1)

            prediction = model.predict(features)[0]
            confidence = model.predict_proba(features)[0][1] * 100

            return render_template('result.html',
                                   approval='Approved' if prediction else 'Rejected',
                                   confidence=round(confidence, 2))

    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
