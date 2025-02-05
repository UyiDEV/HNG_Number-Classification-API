# HNG_Number-Classification-API
Create an API that takes a number and returns interesting mathematical properties about it, along with a fun fact.

In this repository 
 Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application locally:

```
python app.py
```

The API will be available at `http://localhost:5000`.

## API Documentation

### Endpoint: `/api/classify-number`

**Method:** GET

**Query Parameters:**
- `number`: The number to be classified (integer)

**Response:**

The API returns a JSON object with the following properties:

- `number`: The input number
- `is_prime`: Boolean indicating if the number is prime
- `is_perfect`: Boolean indicating if the number is perfect
- `properties`: Array of additional properties (e.g., "armstrong", "odd")
- `digit_sum`: Sum of the digits of the number
- `fun_fact`: A fun fact about the number

**Example:**

Request:
```
GET /api/classify-number?number=153
```

Response:
```json
{
  "number": 153,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "digit_sum": 9,
  "fun_fact": "153 is an Armstrong number because 1^3 + 5^3 + 3^3 = 153"
}
```

## Deployment

This application is designed to be deployed using a WSGI server. The `wsgi.py` file is provided for this purpose.