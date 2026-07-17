import pytest
from falcon import testing
from cart_api.api import api

# Runs after every test function; removes any TestProduct rows the failing assertion left behind -Ian
@pytest.fixture(autouse=True)
def cleanup_test_products():
    yield
    client = testing.TestClient(api)
    response = client.simulate_get('/v1/products')
    if response.json:
        for product in response.json:
            if product.get('name', '').startswith('TestProduct'):
                client.simulate_delete(f'/v1/products/{product["id"]}')
