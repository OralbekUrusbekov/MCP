import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server.main import load_products, save_products


def test_load_save_products():
    data = [{"id": 1, "name": "X", "price": 10, "category": "A", "in_stock": True}]

    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name

    try:
        from unittest.mock import patch

        with patch("mcp_server.main.DATA_FILE", path):
            save_products(data)
            loaded = load_products()
            assert loaded[0]["name"] == "X"

    finally:
        os.unlink(path)
