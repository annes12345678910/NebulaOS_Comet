import ultimateraylib as rl
import requests

class Website:
    def __init__(self, url: str = "https://example.org/") -> None:
        self.url = url

    def connect(self):
        try:
            response = requests.get(
                self.url,
                timeout=5,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            return None

def test():
    opo = Website()
    data = opo.connect()
    if data:
        print("Connected successfully!")
        print(data)  # preview

if __name__ == "__main__":
    test()
