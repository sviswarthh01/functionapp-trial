from fastapi import FastAPI, BackgroundTasks
import httpx, time
import uuid, asyncio
from fastapi.responses import JSONResponse

app = FastAPI()

# Define the Azure Function App endpoint (replace with your actual Azure function URL)
AZURE_FUNCTION_URL = "https://func-processor-kpnloo4efwvaq.azurewebsites.net/api/httpget?code=o8UvpcfNUki-6Oh6NKQNDmQHMXI4RLaMbAJqeHORqcSbAzFuWIzCuA%3D%3D&name=Vish"
# AZURE_FUNCTION_URL = "https://func-processor-kpnloo4efwvaq.azurewebsites.net/api/httpgetwebpage?code=JFrO9rc8SzhzFL9sRtuLqvKtJ4io7jA4rGlWpRpvwwc2AzFuJYrRfA%3D%3D" # For the webpage request

NUM_REQUESTS = 500

# In-memory store to track request status (replace with Redis or database for production use)
request_status = {}

# Function to send 500 requests asynchronously to the Azure Function and measure latency
async def send_requests_to_azure(function_url: str, request_id: str):
    # Connection pool limits
    limits = httpx.Limits(max_connections=NUM_REQUESTS, max_keepalive_connections=100)
    
    # Start the total timer
    start_time = time.perf_counter()

    # Use a custom AsyncClient with higher connection limits
    async with httpx.AsyncClient(limits=limits, timeout=None) as client:
        tasks = []
        latencies = []
        
        for i in range(500):
            # Track time for each request
            tasks.append(make_request_with_latency(client, function_url, latencies))

        # Await all tasks concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Calculate total time for all requests
    total_time = time.perf_counter() - start_time

    # Process responses
    successful_responses = [r for r in responses if isinstance(r, httpx.Response) and r.status_code == 200]
    failed_responses = len([r for r in responses if isinstance(r, httpx.Response) and r.status_code != 200])
    exceptions = [r for r in responses if isinstance(r, Exception)]

    # Mark as completed in the status tracking
    request_status[request_id] = {
        "status": "completed",
        "successful_responses": len(successful_responses),
        "failed_responses": failed_responses,
        "exceptions": len(exceptions),
        "total_time": total_time,
        "average_latency": sum(latencies) / len(successful_responses) if successful_responses else 0,
        "latencies": latencies
    }

    # Log the results for debugging
    print(f"Request ID: {request_id}")
    print(f"Total Time: {total_time}")
    print(f"Average Latency: {request_status[request_id]['average_latency']}")
    print(f"Successful Responses: {len(successful_responses)}")
    print(f"Failed Responses: {failed_responses}")
    print(f"Exceptions: {len(exceptions)}")

# Helper function to track latency for each request
async def make_request_with_latency(client, function_url, latencies):
    start_time = time.perf_counter()  # Start timer for individual request
    try:
        # Replace with POST if needed
        response = await client.get(function_url)
        # Calculate request latency
        latency = time.perf_counter() - start_time
        latencies.append(latency)
        return response
    except Exception as e:
        latencies.append(float('inf'))
        return e

# Endpoint to trigger 500 Azure Function requests
@app.post("/trigger")
async def trigger_azure_requests(background_tasks: BackgroundTasks):
     # Unique ID to track the request
    request_id = str(uuid.uuid4())

    # Initially mark the request as "in progress"
    request_status[request_id] = {"status": "in progress"}

    # Trigger the background task to send requests
    background_tasks.add_task(send_requests_to_azure, AZURE_FUNCTION_URL, request_id)

    # Immediately respond to the client
    return JSONResponse(status_code=200, content={"message": "Request accepted", "request_id": request_id})

# Endpoint to check the status of a previous request
@app.get("/status/{request_id}")
async def check_status(request_id: str):
    if request_id not in request_status:
        return JSONResponse(status_code=404, content={"message": "Request not found"})
    
    return request_status[request_id]

