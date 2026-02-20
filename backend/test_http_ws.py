import urllib.request
import urllib.error

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/ws/dashboard") as response:
        print(f"Status: {response.status}")
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} {e.reason}")
    print(e.read().decode())
except Exception as e:
    print(f"Failed: {e}")
