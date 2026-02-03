import requests
import os

API_URL = "http://127.0.0.1:8000/api/"
FILE_PATH = "sample_equipment_data.csv"

def seed():
    if not os.path.exists(FILE_PATH):
        print(f"File {FILE_PATH} not found.")
        return

    print(f"Uploading {FILE_PATH}...")
    try:
        with open(FILE_PATH, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}upload/", files=files)
            if response.status_code == 201:
                print("Successfully uploaded sample data!")
                print("Response:", response.json())
            else:
                print(f"Failed to upload. Status: {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    seed()
