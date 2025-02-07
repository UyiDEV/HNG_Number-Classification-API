from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n <= 1 or n != int(n):
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_perfect(n):
    if n <= 1 or n != int(n):
        return False
    s = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            s += i
            if i * i != n:
                s += n // i
    return s == n

def is_armstrong(n):
    num_str = str(int(n))
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit)**num_digits for digit in num_str)
    return sum_of_powers == int(n)

def calculate_digit_sum(n):
    return sum(int(digit) for digit in str(abs(int(n))))

def fetch_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "No fun fact available.")
        else:
            return "No fun fact available."
    except requests.exceptions.RequestException:
        return "Error fetching fun fact."

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    number_str = request.args.get("number")
    if number_str is None:
        return jsonify({"error": "No number provided"}), 400

    try:
        number = float(number_str)
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("even" if number % 2 == 0 else "odd")

    return jsonify({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": calculate_digit_sum(number),
        "fun_fact": fetch_fun_fact(number)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)