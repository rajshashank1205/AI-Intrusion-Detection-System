import requests
import time


URL = "http://127.0.0.1:5000/login"


def test_bruteforce_detection():

    print("\nStarting brute-force detector test...")
    print("-" * 50)

    successful_requests = 0

    for i in range(10):

        data = {
            "username": "attacker",
            "password": f"wrongpassword{i}"
        }

        response = requests.post(
            URL,
            data=data,
            timeout=5
        )

        print(
            f"Attempt {i + 1}: "
            f"HTTP {response.status_code}"
        )

        assert response.status_code == 200

        successful_requests += 1

        time.sleep(0.2)

    print("-" * 50)
    print(
        f"Completed {successful_requests}/10 login attempts."
    )

    assert successful_requests == 10