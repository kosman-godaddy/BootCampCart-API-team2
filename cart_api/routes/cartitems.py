import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseCartItem


# Exercise 3:
# Using the database model you created in Exercise 1 create a cartitems route
# CartItems should have a responder for POST and GET
# CartItem should have responders for GET DELETE PATCH
# Your API response statuses and bodies should conform to your OpenAPI spec


class CartItems:
    def on_get(self, req, resp):
        items = DatabaseCartItem.select().order_by(DatabaseCartItem.id)
        resp.media = [model_to_dict(item) for item in items]
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.media
        new_item = DatabaseCartItem.create(**data)
        resp.media = model_to_dict(new_item)
        resp.status = falcon.HTTP_201


class CartItem:
    def on_get(self, req, resp, cart_item_id):
        cart_item = DatabaseCartItem.get(id=cart_item_id)
        resp.media = model_to_dict(cart_item)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, cart_item_id):
        DatabaseCartItem.delete_by_id(cart_item_id)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, cart_item_id):
        cart_item = DatabaseCartItem.get(id=cart_item_id)
        data = req.media
        for key, value in data.items():
            setattr(cart_item, key, value)
        cart_item.save()
        resp.status = falcon.HTTP_204
