__author__ = "Andrew Williamson <axwilliamson@godaddy.com>"

import falcon
from swagger_ui import falcon_api_doc
from cart_api.routes.heartbeat import Heartbeat
from cart_api.routes.products import Product, Products
from cart_api.routes.cartitems import CartItem, CartItems
from cart_api.routes.orders import Order, Orders


# Instantiate RESTful API and resources
api = falcon.App(cors_enable=True)
api.req_options.strip_url_path_trailing_slash = True
hb = Heartbeat()
product = Product()
products = Products()
cartitem = CartItem()
cartitems = CartItems()
order = Order()
orders = Orders()

# Define our API's routes
api.add_route("/heartbeat", hb)
api.add_route("/v1/products/{product_id:int}", product)
api.add_route("/v1/products", products)
api.add_route("/v1/cartitems", cartitems)
api.add_route("/v1/cartitems/{cart_item_id:int}", cartitem)
api.add_route("/v1/orders", orders)
api.add_route("/v1/orders/{order_id:int}", order)

# swagger_ui_py 0.3.0 always registers its index at url_prefix + "/" (trailing slash).
# Falcon's strip_url_path_trailing_slash=True strips that slash before routing, making
# the library's own /docs/ route unreachable. Workaround: store the returned interface
# object and register /docs (no trailing slash) ourselves. -Ian
_swagger = falcon_api_doc(
    api, config_path="/swagger/api.json", url_prefix="/docs", title="Cart API", editor=True
)


class _SwaggerDocs:
    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.text = _swagger.doc_html


api.add_route("/docs", _SwaggerDocs())


# Add custom error handling
def http405(req, resp, error, params):
    """Intercept any 405 type errors and return json"""
    resp.status = falcon.HTTP_405
    resp.media = {
        "code": "405_METHOD_NOT_ALLOWED",
        "message": "Cannot perform " + req.method + " on " + req.url,
    }


api.add_error_handler(falcon.HTTPMethodNotAllowed, http405)
