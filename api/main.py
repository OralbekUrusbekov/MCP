from fastapi import FastAPI
from agent.agent import get_agent

app = FastAPI()
agent = get_agent()


@app.post("/api/v1/agent/query")
async def q(body: dict):
    print("🌐 API CALL:", body)
    return {
        "response": agent.query(body["query"])
    }


@app.get("/api/v1/products")
async def p(category: str | None = None):
    from mcp_server.main import list_products
    print("🌐 PRODUCTS CALL:", category)
    return list_products(category)

@app.get("/")
async def root():
    return {
        "message": "API ready",
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}