from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Twilio credentials (store securely in real apps, e.g., with environment variables)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

TWILIO_VERIFY_SID = os.getenv('TWILIO_VERIFY_SID')

verification = client.verify \
    .v2 \
    .services(TWILIO_VERIFY_SID) \
    .verifications \
    .create(to='+918128176740', channel='sms')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    phone = request.json.get('phone')
    try:
        verification = client.verify.services(TWILIO_VERIFY_SID).verifications.create(
            to=phone, channel='sms'
        )
        return jsonify({'status': verification.status})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    phone = request.json.get('phone')
    code = request.json.get('code')
    try:
        check = client.verify.services(TWILIO_VERIFY_SID).verification_checks.create(
            to=phone, code=code
        )
        return jsonify({'status': check.status})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Important for Render!
