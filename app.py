from flask import Flask, jsonify, request
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def classify_number(n):
    """Classifies a number and returns its properties."""

    try:
        n = int(n)  # Ensure the input is an integer
    except ValueError:
        return jsonify({"number": n, "error": True}), 400

    is_prime = is_prime_number(n)
    is_perfect = is_perfect_number(n)
    properties = []
    if is_armstrong_number(n):
        properties.append("armstrong")
    if n % 2 != 0:
        properties.append("odd")
    digit_sum = sum(int(digit) for digit in str(n))
    fun_fact = get_fun_fact(n, properties)

    return jsonify({
        "number": n,
        "is_prime": is_prime,
        "is_perfect": is_perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }), 200


def is_prime_number(n):
    """Checks if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect_number(n):
    """Checks if a number is perfect."""
    if n <= 1:
        return False
    sum_of_divisors = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_of_divisors += i + n // i
    return sum_of_divisors == n

def is_armstrong_number(n):
  """Checks if a number is an Armstrong number."""
  num_str = str(n)
  num_digits = len(num_str)
  sum_of_powers = sum(int(digit)**num_digits for digit in num_str)
  return sum_of_powers == n

def get_fun_fact(n, properties):
    """Generates a fun fact about the number."""
    if "armstrong" in properties:
        num_str = str(n)
        power = len(num_str)
        calculation = " + ".join(f"{digit}^{power}" for digit in num_str)
        return f"{n} is an Armstrong number because {calculation} = {n}"
    elif is_prime_number(n):
      return f"{n} is a prime number."
    else:
      return f"{n} is a number."


@app.route('/api/classify-number', methods=['GET'])
def api_classify_number():
    number = request.args.get('number')
    return classify_number(number)


