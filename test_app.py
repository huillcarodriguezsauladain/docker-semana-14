import unittest
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_analizar_texto_valido(self):
        payload = {
            "texto": "Docker es una herramienta increible para el despliegue de aplicaciones"
        }
        response = self.client.post("/analizar", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["palabras"], 10)
        self.assertEqual(data["frecuencia"]["docker"], 1)
        self.assertEqual(data["resumen"], payload["texto"])

    def test_analizar_texto_vacio(self):
        response = self.client.post("/analizar", json={"texto": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_analizar_texto_solo_espacios(self):
        response = self.client.post("/analizar", json={"texto": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Texto vacio")

    def test_analizar_json_invalido_o_ausente(self):
        response = self.client.post("/analizar", data="no es json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_analizar_tipo_texto_invalido(self):
        response = self.client.post("/analizar", json={"texto": 12345})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Texto vacio")


if __name__ == "__main__":
    unittest.main()
