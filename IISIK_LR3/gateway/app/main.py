from __future__ import annotations

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .clients.factory import build_clients
from .config import settings
from .schema.schema import schema

clients = build_clients(settings)


async def context_getter() -> dict[str, object]:
    return {"clients": clients, "cache": {}}


graphql_app = GraphQLRouter(
    schema,
    context_getter=context_getter,
    graphql_ide="graphiql",
)

app = FastAPI(
    title="GraphQL Gateway — динамическое ценообразование",
    version="1.0.0",
)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "gateway", "client_mode": settings.client_mode}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "gateway",
        "status": "ok",
        "graphql": "/graphql",
        "docs": "/docs",
        "health": "/health",
    }
