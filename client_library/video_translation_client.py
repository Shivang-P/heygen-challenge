import requests
import time

class VideoTranslationClient:
    def __init__(self, base_url, max_retries=10, max_wait_time=60):
        self.base_url = base_url
        self.max_retries = max_retries
        self.max_wait_time = max_wait_time

    def set_completion_time(self, completion_time):
        """
        Sends a POST request to set the completion time on the server.
        """
        try:
            response = requests.post(
                f"{self.base_url}/set_completion_time", 
                json={"completion_time": completion_time}
            )
            if response.status_code == 200:
                print(f"Completion time set to {completion_time} seconds.")
            else:
                print(f"Failed to set completion time: {response.text}")
        except requests.RequestException as e:
            print(f"Error setting completion time: {e}")

    def get_status(self):
        retries = 0
        wait_time = 1  # Initial wait time in seconds

        while retries < self.max_retries:
            try:
                response = requests.get(f"{self.base_url}/status")
                result = response.json().get("result")
                
                if result in ["completed", "error"]:
                    return result
                
                # If result is "pending", wait before retrying
                time.sleep(wait_time)
                wait_time = min(wait_time * 2, self.max_wait_time)
                retries += 1
            
            except requests.RequestException as e:
                print(f"Error fetching status: {e}")
                return "error"

        return "error"  # If all retries are exhausted, return error

# Usage
client = VideoTranslationClient("http://localhost:5000")
client.set_completion_time(5)
status = client.get_status()
print(f"Final Status: {status}")
