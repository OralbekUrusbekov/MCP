import re
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END


from mcp_server.main import list_products, get_product, add_product, get_statistics




class AgentState(TypedDict):
    query: str
    messages: List[Dict[str, Any]]
    response: str
    current_data: Optional[Dict[str, Any]]





class MockLLM:
    def invoke(self, messages):
        text = messages[-1]["content"].lower()

        if "покажи" in text:
            return {"content": "list_products"}
        if "стат" in text:
            return {"content": "get_statistics"}
        if "добав" in text:
            return {"content": "add_product"}
        if "id" in text:
            return {"content": "get_product"}
        if "скид" in text or "discount" in text:
            return {"content": "calculate_discount"}

        return {"content": "help"}




class ProductAgent:

    def __init__(self):
        self.llm = MockLLM()
        self.graph = self._build()

    def _build(self):
        g = StateGraph(AgentState)
        g.add_node("analyze", self._analyze)
        g.add_node("tool", self._tool)
        g.add_node("format", self._format)

        g.set_entry_point("analyze")
        g.add_edge("analyze", "tool")
        g.add_edge("tool", "format")
        g.add_edge("format", END)

        return g.compile()

    def _analyze(self, state):
        q = state["query"]
        state["messages"] = [{"role": "user", "content": q}]
        action = self.llm.invoke(state["messages"])["content"]

        state["current_data"] = {"action": action, "query": q}
        return state

    def _extract(self, q):
        info = {}
        if "электроника" in q.lower():
            info["category"] = "Электроника"

        nums = re.findall(r"\d+", q)
        if nums:
            info["id"] = int(nums[0])

        return info

    def _tool(self, state):
        action = state["current_data"]["action"]
        q = state["current_data"]["query"]
        info = self._extract(q)

        if action == "list_products":
            result = list_products(info.get("category"))

        elif action == "get_product":
            result = get_product(info.get("id", 1))

        elif action == "add_product":
            result = add_product("Мышка", 1500, "Электроника")

        elif action == "get_statistics":
            result = get_statistics()

        else:
            result = {"msg": "help"}

        state["current_data"]["result"] = result
        return state

    def _format(self, state):
        result = state["current_data"]["result"]
        state["response"] = str(result)
        return state

    def query(self, q):
        out = self.graph.invoke({
            "query": q,
            "messages": [],
            "response": "",
            "current_data": None
        })

        return out["response"]


_agent = None

def get_agent():
    global _agent
    if not _agent:
        _agent = ProductAgent()
    return _agent
