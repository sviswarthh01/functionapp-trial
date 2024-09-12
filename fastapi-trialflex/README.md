# FastAPI Request Dispatcher

This FastAPI application is designed to send multiple HTTP requests concurrently to a specified Azure Function App endpoint and measure the latency and total time taken for all requests.

## Features

- Sends multiple HTTP requests concurrently.
- Measures the latency of each request and average latency for all requests.
- Calculates the total time taken for all requests.
- Implements error handling and logging for failed requests.

## Requirements

- Python 3.7+
- FastAPI
- httpx
- uvicorn

## Installation

  1. Clone the repository:

    ```shell
    git clone https://github.com/yourusername/fastapi-request-dispatcher.git
    cd fastapi-request-dispatcher
    ```

  2. Create a virtual environment and activate it:
      ```shell
      python -m venv venv
      .\venv\Scripts\activate   # On Windows
      source venv/bin/activate  # On macOS/Linux
      ```

  3. Install the required dependencies:
     
     ```shell
     pip install -r requirements.txt
     ```

## Configuration
Replace the AZURE_FUNCTION_URL in webapp.py with your actual Azure Function App endpoint URL.

```python
AZURE_FUNCTION_URL = "https://your-azure-function-url"
```

## Usage
   1. Run the FastAPI application using uvicorn:

       ```shell
       uvicorn webapp:app --port 8181 --reload
       ```

    2. Trigger the dispatch of requests by accessing the /trigger endpoint:
   
        ```shell
        curl -X POST "http://localhost:8181/trigger"
        ```
    3. Check the status of the requests by accessing the /status/{request_id} endpoint:
   
        ```shell
        curl -X GET "http://localhost:8181/status/{request_id}"
        ```

    4. The response will include the total time taken for all requests, the average latency per request, and the results of individual requests.

        ### Example Response
        ```json
        {
            "message": "Request accepted",
            "request_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```

        #### To Check the Status
        ```json
        {
            "status": "completed",
            "successful_responses": 500,
            "failed_responses": 0,
            "exceptions": 0,
            "total_time": 120.5,
            "average_latency": 0.24,
            "latencies": [0.23, 0.25, ...]
        }
        ```