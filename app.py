from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests
import json

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
    if n < 0:  # Handle negative numbers correctly
        n = abs(n)
    num_str = str(n)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit)**num_digits for digit in num_str)
    return sum_of_powers == n

def calculate_digit_sum(n):
    if n < 0:  # Handle negative numbers correctly
        n = abs(n)
    return sum(int(digit) for digit in str(n))

def fetch_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        response.raise_for_status()  # Check for HTTP errors

        try:
            data = response.json()
            return data.get("text", "No fun fact available.")
        except json.JSONDecodeError:
            return "Error: Invalid JSON response from fun fact API"

    except requests.exceptions.RequestException as e:
        return f"Error fetching fun fact: {e}"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')

    if not number_str:
        return jsonify({"error": "Number parameter is required"}), 400

    try:
        num = float(number_str)
    except ValueError:
        return jsonify({"number": number_str, "error": True}), 400

    if math.isnan(num) or math.isinf(num):
        return jsonify({"number": number_str, "error": True}), 400

    is_integer = num.is_integer()

    prime = is_prime(int(abs(num))) if is_integer else False
    perfect = is_perfect(int(abs(num))) if is_integer else False
    armstrong = is_armstrong(int(abs(num))) if is_integer else False
    digit_sum = calculate_digit_sum(int(abs(num))) if is_integer else None
    properties = []
    if armstrong:
        properties.append("armstrong")
    if is_integer:
        if num % 2 != 0:
            properties.append("odd")
        else:
            properties.append("even")

    fun_fact = fetch_fun_fact(int(num)) if is_integer else "Fun facts are only available for integers"

    try:  # Wrap the entire response creation in a try...except
        response_data = {
            "number": num,
            "is_prime": prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
        return jsonify(response_data), 200
    except Exception as e: # Catch any JSON serialization errors
        print(f"Error creating JSON response: {e}") #Print error for debugging
        return jsonify({"error": "An error occurred while creating the response."}), 500  # Return a 500 error

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Host for EC2
