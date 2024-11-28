from flask import Flask, render_template, request, jsonify
import qrcode
import random
import io
import base64

app = Flask(__name__)

# Global variable to store OTP
current_otp = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    global current_otp
    current_otp = random.randint(100000, 999999)
    return jsonify({"otp": current_otp})

@app.route('/process_payment', methods=['POST'])
def process_payment():
    upi_id = request.form['upi_id']
    amount = request.form['amount']
    otp = request.form['otp']

    if otp == str(current_otp):
        return jsonify({"message": "Payment Successful", "status": "success"})
    else:
        return jsonify({"message": "Invalid OTP", "status": "error"})

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    amount = request.form['amount']
    
    # Create a QR code with a simple UPI payment URL (replace with actual logic)
    upi_url = f"upi://pay?pa=example@upi&pn=BharatPay&mc=1234&tid=5678&tr={random.randint(1000, 9999)}&tn=Payment%20Request&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)
    
    # Convert the QR code image to a base64 string
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    # Return the base64 string as JSON response
    return jsonify({"status": "success", "qr_image": img_base64})

if __name__ == '__main__':
    app.run(debug=True)
