import falcon
import json
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseOrder


class Orders:
    def on_get(self, req, resp):
        orders = DatabaseOrder.select().order_by(DatabaseOrder.id.desc())
        result = []
        for order in orders:
            d = model_to_dict(order)
            d['items'] = json.loads(order.items)
            result.append(d)
        resp.media = result
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.media
        new_order = DatabaseOrder.create(
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            payment=data.get('payment', ''),
            total=data.get('total', 0),
            items=json.dumps(data.get('items', [])),
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
        result = model_to_dict(new_order)
        result['items'] = json.loads(new_order.items)
        resp.media = result
        resp.status = falcon.HTTP_201


class Order:
    def on_get(self, req, resp, order_id):
        order = DatabaseOrder.get(id=order_id)
        result = model_to_dict(order)
        result['items'] = json.loads(order.items)
        resp.media = result
        resp.status = falcon.HTTP_200
