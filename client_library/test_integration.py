from video_translation_client import VideoTranslationClient

def test_integration():
    client = VideoTranslationClient(
        base_url="http://localhost:5000",
        max_retries=5,
        max_wait_time=60,
        timeout=20,
        retry_on_error=False
    )

    status = client.get_status()
    status_history = client.get_status_history()

    print(f"Final Status: {status}")
    print("Status History:")
    for entry in status_history:
        print(entry)

if __name__ == '__main__':
    test_integration()