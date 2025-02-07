from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import math
import requests

app = FastAPI(title="Number Classification API")

# Enable CORS (customize origins as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
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

def is_perfect(n: int) -> bool:
    if n <= 1:
        return False
    s = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            s += i
            if i * i != n:
                s += n // i
    return s == n

def is_armstrong(n: int) -> bool:
    if n < 0:
        n = abs(n)
    num_str = str(n)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit)**num_digits for digit in num_str)
    return sum_of_powers == n

def calculate_digit_sum(n: int) -> int:
    if n < 0:
        n = abs(n)
    return sum(int(digit) for digit in str(n))

def fetch_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        response.raise_for_status()  # Check for HTTP errors

        try:
            data = response.json()
            return data.get("text", "No fun fact available.")
        except (requests.exceptions.JSONDecodeError, json.JSONDecodeError):  # Handle JSON errors
            return "Error: Invalid JSON response from fun fact API"
    except requests.exceptions.RequestException as e:
        return f"Error fetching fun fact: {e}"

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        num = float(number)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})

    if math.isnan(num) or math.isinf(num):
        raise HTTPException(status_code=400, detail={"number": number, "error": True})


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

    return {
        "number": num,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
