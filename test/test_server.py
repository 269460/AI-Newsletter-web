import requests


def test_server():
    base_url = "http://localhost:5000"  # Zmień, jeśli Twój serwer działa na innym porcie

    # Test strony głównej
    response = requests.get(f"{base_url}/")
    print("Home page status code:", response.status_code)

    # Test strony kategorii
    response = requests.get(f"{base_url}/category/AI")
    print("Category page status code:", response.status_code)

    # Test strony artykułu (zakładając, że masz artykuł o ID 1)
    response = requests.get(f"{base_url}/article/1")
    print("Article page status code:", response.status_code)


if __name__ == "__main__":
    test_server()