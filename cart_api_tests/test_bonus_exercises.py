from .test_heartbeat import TestClient


class BonusExercise(TestClient):
    def test_create_order(self):
        # POST a new order and verify the response contains what we sent -Ian
        new_order = {
            "name": "Ian Nortey",
            "email": "ian@example.com",
            "phone": "555-1234",
            "payment": "credit_card",
            "total": 49.99,
            "items": [{"id": 1, "name": "Standard SSL", "quantity": 1}],
        }
        response = self.simulate_post("/v1/orders", json=new_order)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], new_order["name"])
        self.assertEqual(response.json["total"], new_order["total"])
        self.assertIsInstance(response.json["items"], list)

    def test_get_orders_returns_list(self):
        # GET all orders and verify the response is a list -Ian
        response = self.simulate_get("/v1/orders")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
