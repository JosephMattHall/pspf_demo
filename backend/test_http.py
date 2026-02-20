import urllib.request

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/health") as response:
        print(f"Status: {response.status}")
        print(response.read().decode())
except Exception as e:
    print(f"Failed: {e}")
