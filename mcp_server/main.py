import json
import os
from typing import List, Dict, Any, Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "products.json")


def load_products() -> List[Dict[str, Any]]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_products(products: List[Dict[str, Any]]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)



def list_products(category: Optional[str] = None):
    products = load_products()
    if category:
        return [p for p in products if p["category"].lower() == category.lower()]
    return products


def get_product(product_id: int):
    for p in load_products():
        if p["id"] == product_id:
            return p
    raise ValueError("Not found")


def add_product(name: str, price: float, category: str, in_stock: bool = True):
    products = load_products()
    new_id = max([p["id"] for p in products], default=0) + 1

    new_product = {
        "id": new_id,
        "name": name,
        "price": price,
        "category": category,
        "in_stock": in_stock
    }

    products.append(new_product)
    save_products(products)
    return new_product


def get_statistics():
    products = load_products()
    total = len(products)

    if total == 0:
        return {"total_products": 0}

    avg = sum(p["price"] for p in products) / total

    return {
        "total_products": total,
        "average_price": round(avg, 2)
    }
