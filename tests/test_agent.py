import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agent.tools import CalculatorTool, FormatterTool
from agent.agent import MockLLM, ProductAgent


def test_calculator_tool():
    calc = CalculatorTool()

    d = calc.calculate_discount(1000, 10)
    assert d["final_price"] == 900

    t = calc.add_tax(1000, 20)
    assert t["total_price"] == 1200


def test_formatter_tool():
    fmt = FormatterTool()

    products = [
        {"id": 1, "name": "Test", "price": 100, "category": "A", "in_stock": True}
    ]

    out = fmt.format_product_list(products)

    assert "Test" in out
    assert "ID: 1" in out

    empty = fmt.format_product_list([])
    assert "табылмады" in empty.lower()


def test_mock_llm():
    llm = MockLLM()

    assert llm.invoke([{"content": "покажи"}])["content"] == "list_products"
    assert llm.invoke([{"content": "статистика"}])["content"] == "get_statistics"
    assert llm.invoke([{"content": "добавь"}])["content"] == "add_product"
    assert llm.invoke([{"content": "скидка"}])["content"] == "calculate_discount"
    assert llm.invoke([{"content": "что это"}])["content"] == "help"


def test_agent_init():
    agent = ProductAgent()
    assert agent is not None
    assert agent.graph is not None


def test_agent_query_runs():
    agent = ProductAgent()
    r = agent.query("покажи продукты")
    assert isinstance(r, str)
