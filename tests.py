from fastapi import responses
from fastapi.testclient import TestClient
import pytest
import json

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

def test_methods():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

def test_auth():
    response = client.get("/auth", params={"password": "siema", "password_hash": "638b2488c3e94d6d6f73f8e875f99aa62325152885aa81441b8315245264cebf2b090b60cfe7591a892798094809437915061cb9dd939d6cd35e6a370df669f3"})
    assert response.status_code == 204

def test_signup():
    response = client.post("/register", data=json.dumps({"name": "Siurek", "surname": "Wiórek"}))
    assert response.status_code == 200
    assert response.json() == {"name": "Siurek", "surname": "Wiórek"}


import unittest

from file import is_palindrome


class ExampleTest(unittest.TestCase):
    @is_palindrome
    def show_sentence(self):
        return "annA"

    def test_result(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")


if __name__ == "__main__":
    unittest.main()