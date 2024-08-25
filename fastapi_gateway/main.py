import secrets
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from keycloak import KeycloakOpenID

app = FastAPI()

secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

KEYCLOAK_SERVER_URL = "https://auth.civmillabs.com/"
KEYCLOAK_REALM = "civmillabs"
KEYCLOAK_CLIENT_ID = "api"
KEYCLOAK_CLIENT_SECRET = "0Wrdh3lkRWzMJ56AW7532Td8uCDTt5rx"
REDIRECT_URI = "https://api.civmillabs.com/callback"

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    verify=True,
)


@app.get("/login")
async def login():
    auth_url = keycloak_openid.auth_url(redirect_uri=REDIRECT_URI, scope="openid")
    return RedirectResponse(url=auth_url)


@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    token = keycloak_openid.token(
        grant_type="authorization_code", code=code, redirect_uri=REDIRECT_URI
    )

    request.session["access_token"] = token["access_token"]

    return RedirectResponse(url="https://civmillabs.com")


@app.get("/protected")
async def protected(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"message": "Access granted", "token": access_token}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
