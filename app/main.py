from fastapi import FastAPI
from .db import Base, engine
from .users import routes as user_routes
from .clients import routes as client_routes
from .auth import auth as authorize_route
from .auth import token as token_route
from .resources import routes as resource_routes
# from .debug import test as debug_routes
from .auth import introspect as introspect_route
from .auth import revoke as revoke_route
from .well_known import routes as well_known_routes


app = FastAPI(title="Mini OAuth2 Authorization Server")
Base.metadata.create_all(bind=engine)


app.include_router(user_routes.router)
app.include_router(client_routes.router)
app.include_router(authorize_route.router)
app.include_router(token_route.router)
app.include_router(resource_routes.router)
# app.include_router(debug_routes.router)
app.include_router(introspect_route.router)
app.include_router(revoke_route.router)
app.include_router(well_known_routes.router)


@app.get("/")
def root():
    return {"message": "OAuth2 Server running!"}