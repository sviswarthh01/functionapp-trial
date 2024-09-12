---
name: Azure Functions Python HTTP Trigger using azd
description: This repository contains an Azure Functions HTTP trigger written in Python and deployed to Azure Functions Flex Consumption using the Azure Developer CLI (azd).
languages:
- azdeveloper
- python
- bicep
products:
- azure
- azure-functions
- entra-id
urlFragment: functions-trialflex
---

## Prerequisites

+ [Python 3.11](https://www.python.org/)
+ [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools)
+ [Azure Developer CLI (AZD)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)

## Create a virtual environment

The way that you create your virtual environment depends on your operating system.
Open the terminal, navigate to the project folder, and run these commands:

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```shell
py -m venv .venv
.venv\scripts\activate
```

## Run your app from the terminal

1. Run these commands in the virtual environment:

    ```shell
    pip3 install -r requirements.txt
    func start
    ```

2. From your HTTP test tool in a new terminal (or from your browser), call the HTTP GET endpoint: <http://localhost:7071/api/httpget>

3. Test the HTTP POST trigger with a payload using your favorite secure HTTP test tool. This example uses the `curl` tool with payload data from the [`testdata.json`](./testdata.json) project file:

    ```shell
    curl -i http://localhost:7071/api/httppost -H "Content-Type: text/json" -d @testdata.json
    ```

## Source Code

The source code for both functions is in `function_app.py` code file. The function is identified as an Azure Function by use of the `@azure/functions` library. This code shows an HTTP GET triggered function.  

```python
@app.route(route="httpget", methods=["GET"])
def http_get(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "World")

    logging.info(f"Processing GET request. Name: {name}")

    return func.HttpResponse(f"Hello, {name}!")
```

This code shows an HTTP POST triggered function.

```python
@app.route(route="httppost", methods=["POST"])
def http_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        name = req_body.get('name')
        age = req_body.get('age')
        
        logging.info(f"Processing POST request. Name: {name}")

        if name and isinstance(name, str) and age and isinstance(age, int):
            return func.HttpResponse(f"Hello, {name}! You are {age} years old!")
        else:
            return func.HttpResponse(
                "Please provide both 'name' and 'age' in the request body.",
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body",
            status_code=400
        )
```

This code shows an HTTP GET triggered function which hits a webpage and returns the response.

```python
@app.route(route="httpgetwebpage", methods=["GET"])
def http_get_webpage(req: func.HttpRequest) -> func.HttpResponse:
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)

    if response.status_code == 200:
        return func.HttpResponse(response.text, status_code=200, mimetype="application/json")
    else:
        return func.HttpResponse("Failed to fetch data", status_code=response.status_code)
```

## Deploy to Azure

Run this command to provision the function app, with any required Azure resources, and deploy your code:

```shell
azd up
```

You're prompted to supply these required deployment parameters:

| Parameter | Description |
| ---- | ---- |
| _Environment name_ | An environment that's used to maintain a unique deployment context for your app. You won't be prompted if you created the local project using `azd init`.|
| _Azure subscription_ | Subscription in which your resources are created.|
| _Azure location_ | Azure region in which to create the resource group that contains the new Azure resources. Only regions that currently support the Flex Consumption plan are shown.|

## Redeploy your code

You can run the `azd up` command as many times as you need to both provision your Azure resources and deploy code updates to your function app. 

>[!NOTE]
>Deployed code files are always overwritten by the latest deployment package.

## Clean up resources

When you're done working with your function app and related resources, you can use this command to delete the function app and its related resources from Azure and avoid incurring any further costs:

```shell
azd down
```
