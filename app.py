from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n <= 1:
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
    if n <= 1:
        return False
    s = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            s += i
            if i * i != n:
                s += n // i
    return s == n

def is_armstrong(n):
    num_str = str(n)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit)**num_digits for digit in num_str)
    return sum_of_powers == n

def calculate_digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))

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

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "Number parameter is required"}), 200

    try:
        num = int(number)
    except ValueError:
        return jsonify({"number": number, "error": True}), 200

    prime = is_prime(num)
    perfect = is_perfect(num)
    armstrong = is_armstrong(num)
    digit_sum = calculate_digit_sum(num)
    properties = []
    if armstrong:
        properties.append("armstrong")
    if num % 2 != 0:
        properties.append("odd")
    else:
        properties.append("even")

    fun_fact = fetch_fun_fact(num)

    return jsonify({
        "number": num,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)