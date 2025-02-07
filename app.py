from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Adding CORS Middleware to allow cross-origin requests
origins = ["*"]  # This allows all origins; you can restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number: int) -> bool:
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def is_armstrong(number: int) -> bool:
    digits = list(map(int, str(number)))
    power = len(digits)
    return number == sum([digit ** power for digit in digits])

def get_fun_fact(number: int) -> str:
    url = f"http://numbersapi.com/{number}?json"
    response = requests.get(url).json()
    return response.get('text', 'No fun fact available')

@app.get("/api/classify-number")
async def classify_number(number: str):
    try:
        num = int(number)  # Input validation
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})

    # Determine properties
    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    if num % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Prepare the response JSON
    response_data = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum([int(digit) for digit in str(num)]),
        "fun_fact": get_fun_fact(num)
    }

    return JSONResponse(content=response_data)


