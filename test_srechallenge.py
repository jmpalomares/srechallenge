import unittest
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_get_responseA(self):
        response = self.client.get("/srechallenge?saludation=Hi")
        assert response.status_code == 200

    def test_get_responseB(self):
        response = self.client.get("/srechallenge?saludation=Dear Sir or Madam")
        assert response.status_code == 200

    def test_get_responseC(self):
        response = self.client.get("/srechallenge?saludation=Moin")
        assert response.status_code == 200

    def test_get_responseBad(self):
        response = self.client.get("/srechallenge")
        assert response.status_code == 500


if __name__ == "__main__":
    unittest.main()
