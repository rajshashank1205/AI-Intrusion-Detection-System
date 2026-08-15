import requests
import time

URL = "http://127.0.0.1:5000/login"

print("Starting brute-force detector test...")
print("-" * 50)

for i in range(10):
    data = {
        "username": "attacker",
        "password": f"wrongpassword{i}"
    }

    response = requests.post(URL, data=data)

    print(
        f"Attempt {i + 1}/10 | "
        f"Status: {response.status_code}"
    )

    time.sleep(0.5)

print("-" * 50)
print("Brute-force test completed.")