# Video Translation Client Library

This repository contains a Python client library to interact with a simulated video translation service, designed to allow users to poll for the status of a translation job with customizable retry, wait, and timeout configurations. This client is suitable for handling the asynchronous nature of video translation, minimizing API calls while avoiding unnecessary delays.

## Table of Contents
- [Installation](#installation)
- [Server Setup](#server-setup)
- [Client Library](#client-library)
- [Usage](#usage)
- [Integration Test](#integration-test)
- [Configuration Flags](#configuration-flags)
- [Features](#features)
- [Future/Production Considerations](#futureproduction-considerations)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Shivang-P/heygen-challenge.git
   cd heygen-challenge
   ```

2. Install Flask:
    ```bash
    pip install flask
    ```

## Server Setup
The server simulates the video translation backend with an endpoint that returns the job status and an endpoint for setting the completion time, allowing testing of various delay scenarios.

To start the server, first navigate to the server folder and then run the server file:
```bash
cd server
python server.py
```
### Endpoints
- **`GET /status`**: Returns the current status of the translation job. Possible responses are:
  - `pending`: The job is still processing.
  - `completed`: The job has finished successfully.
  - `error`: An error occurred in processing.

- **`POST /set_completion_time`**: Sets the completion time for the translation job on the server. This is useful for testing different scenarios in the client library. Accepts a JSON body:
  ```json
  { "completion_time": 15 }

## Client Library

The client library, `VideoTranslationClient`, provides methods to interact with the server, configure retries, set a completion time, and log status history. 

### Configuration Flags
- `base_url`: URL used to fetch status from, defaulted to localhost.
- `max_retries`: Maximum number of retries for polling the status.
- `max_wait_time`: Maximum wait time between retries, with exponential backoff.
- `timeout`: Total time to wait for a status change from `pending` to `completed/error`.
- `retry_on_error`: Whether to retry if an `error` status is received.

### Usage

1. **Instantiate the Client**  
   ```python
   from video_translation_client import VideoTranslationClient

   client = VideoTranslationClient(
       base_url="http://localhost:5000",
       max_retries=5,
       max_wait_time=60,
       timeout=20,
       retry_on_error=True
   )

2. **Set Completion Time**  
Optionally, set a custom completion time on the server to simulate different scenarios:
   ```python
   client.set_completion_time(10)
   ```

3. **Get Job Status**  
Start checking the job status, which will retry as configured:
   ```python
   status = client.get_status()
   print(f"Final Status: {status}")
   ```

4. **Get Status History**  
Track all status checks made by the client during the session:
   ```python
   history = client.get_status_history()
   for entry in history:
        print(entry)
   ```

## Integration Test
An integration test, `test_integration.py`, demonstrates using the client library to check status and retrieve a full log of the status history. To run it, navigate to the `client_library` folder and execute:
```bash
cd client_library
python test_integration.py
```

## Features

This client library includes several advanced features designed to enhance usability and flexibility for users:

### 1. Completion Time Configuration
Users can set a custom completion time for the video translation job directly from the client library, allowing for the simulation of different processing scenarios during testing.

### 2. Exponential Backoff for Consecutive Requests
The client employs an exponential backoff strategy when polling for job status. This means the wait time between consecutive requests increases exponentially, helping to reduce server load while allowing for efficient polling.

### 3. Max Retries for Consecutive Calls
Users can specify the maximum number of retries for consecutive status checks. This prevents the client from endlessly polling the server in cases where the job takes longer than expected or encounters issues.

### 4. Retry on Error Flag
The `retry_on_error` flag (default: `False`) allows users to control whether the client should retry requests that result in an error status, providing flexibility in managing error handling strategies.

### 5. Status History Tracking
The client keeps a detailed history of all status checks made during its operation, including timestamps and responses. This feature is beneficial for logging and debugging, allowing users to review how the status has changed over time.

## Future/Production Considerations

### 1. Estimated Time Remaining
In future versions of the client library, we plan to implement a method that provides users with the estimated time remaining for video translation jobs. This feature can enhance the user experience by allowing for progress tracking, making it easier for users to manage their expectations regarding job completion.

### 2. Asynchronous Support
To improve performance and responsiveness, especially in production environments, we may consider adding asynchronous support. This would allow users to perform other tasks while waiting for the status updates, significantly enhancing the library's usability.

### 3. Error Handling Enhancements
Further enhancements in error handling can be implemented, including more granular error responses from the server and user-friendly messages that guide users on possible corrective actions.

### 4. Store ENV Variables
On a production environment, we would want to store important information such as URLs, API Keys, etc in a config instead of using strings.

### 5. Caching
For API calls to a server, caching can be used to reduce the amount of calls made, the time it takes for the data to reach the user and prevent overloading the server.

### 6. Authentication/Authorization
Given that in a real world case, the video translation is a costly call to the API, it is important the access to the server is guarded using authentication and authorization of some sort (ex. role-based)