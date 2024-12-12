import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )
    
    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/5/10"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "50", "ERROR MULTIPLY"
        )
    
    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/5/10"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "0.5", "ERROR DIVIDE"
        )

    def test_api_divide_by_zero(self):
        # Construimos la URL para dividir por cero
        url = f"{BASE_URL}/calc/divide/5/0"
        try:
            # Hacemos la petición
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail(f"La API no devolvió un error HTTP 406 para {url}")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.NOT_ACCEPTABLE,
                f"Se esperaba HTTP 406, pero se recibió {e.code} para {url}"
            )
            self.assertIn(
                "Division by zero", e.reason,
                "El mensaje de error no contiene 'Division by zero'"
            )

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
