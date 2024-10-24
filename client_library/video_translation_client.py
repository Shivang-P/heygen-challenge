import requests
import time

class VideoTranslationClient:
    def __init__(self, base_url, max_retries=10, max_wait_time=60):
        self.base_url = base_url
        self.max_retries = max_retries
        self.max_wait_time = max_wait_time

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
status = client.get_status()
print(f"Final Status: {status}")
