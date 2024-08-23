from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient
import jwt
from typing import Annotated

app = FastAPI()

# Mount the static directory for serving HTML files at /static
app.mount("/static", StaticFiles(directory="static"), name="static")


# Serve index.html directly at the root
@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")


# OAuth2 settings
oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://auth.civmillabs.com/realms/civmillabs/protocol/openid-connect/token",
    authorizationUrl="http://auth.civmillabs.com/realms/civmillabs/protocol/openid-connect/auth",
    refreshUrl="http://auth.civmillabs.com/protocol/openid-connect/token",
)


async def valid_access_token(access_token: Annotated[str, Depends(oauth_2_scheme)]):
    url = "http://auth.civmillabs.com/realms/civmillabs/protocol/openid-connect/certs"
    jwks_client = PyJWKClient(url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/public")
def get_public():
    return {"message": "This endpoint is public"}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "This endpoint is private"}


@app.get("/login")
def login():
    return RedirectResponse(
        url="http://auth.civmillabs.com/realms/civmillabs/protocol/openid-connect/auth?client_id=api&response_type=code&redirect_uri=https://civmillabs.com"
    )
