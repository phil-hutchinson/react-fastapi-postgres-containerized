import time
import json
import base64
from typing import List, Optional
from urllib.parse import urlencode

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from jose import jwt

app = FastAPI(title="Dev OIDC")

# In dev only. Do not use in prod.
ISSUER = "http://localhost:8088"
CLIENT_ID = "dev-client"
CLIENT_SECRET = "dev-secret"
REDIRECT_URI = "http://localhost:3000/callback"  # adjust to your frontend callback
JWT_SECRET = "dev-jwt-secret-change-me"
JWT_ALG = "HS256"

HTML_TEMPLATE = """
<html>
  <body style="font-family: sans-serif; max-width: 640px; margin: 40px auto;">
    <h2>Dev OIDC Login</h2>
    <form method="post" action="/consent">
      <input type="hidden" name="state" value="{state}" />
      <input type="hidden" name="client_id" value="{client_id}" />
      <input type="hidden" name="redirect_uri" value="{redirect_uri}" />
      <p>Select roles to include in your token:</p>
      <label><input type="checkbox" name="roles" value="reader" checked> reader</label><br/>
      <label><input type="checkbox" name="roles" value="editor"> editor</label><br/>
      <label><input type="checkbox" name="roles" value="admin"> admin</label><br/>
      <p>
        <label>Username (sub/email): <input type="text" name="username" value="dev@example.com"/></label>
      </p>
      <button type="submit">Login & Consent</button>
    </form>
  </body>
</html>
"""

@app.get("/.well-known/openid-configuration")
def well_known():
    return {
        "issuer": ISSUER,
        "authorization_endpoint": f"{ISSUER}/authorize",
        "token_endpoint": f"{ISSUER}/token",
        "jwks_uri": f"{ISSUER}/.well-known/jwks.json",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "id_token_signing_alg_values_supported": [JWT_ALG],
    }

@app.get("/.well-known/jwks.json")
def jwks():
    # HS256 doesn't expose public key; provide a dummy for tooling compatibility.
    return {"keys": []}

@app.get("/authorize")
def authorize(response_type: str, client_id: str, redirect_uri: str, scope: str = "openid profile email", state: Optional[str] = None, code_challenge: Optional[str] = None, code_challenge_method: Optional[str] = None):
    # Display a simple role selection/consent page
    html = HTML_TEMPLATE.format(state=state or "", client_id=client_id, redirect_uri=redirect_uri)
    return HTMLResponse(html)

@app.post("/consent")
async def consent(state: str = Form(None), client_id: str = Form(...), redirect_uri: str = Form(...), roles: Optional[List[str]] = Form(None), username: str = Form("dev@example.com")):
    # Generate a short-lived auth code that encodes the chosen roles
    code_payload = {
        "roles": roles or ["reader"],
        "username": username,
        "ts": int(time.time())
    }
    code = base64.urlsafe_b64encode(json.dumps(code_payload).encode()).decode()
    params = {"code": code}
    if state:
        params["state"] = state
    return RedirectResponse(url=f"{redirect_uri}?{urlencode(params)}", status_code=302)

@app.post("/token")
async def token(grant_type: str = Form(...), code: str = Form(None), redirect_uri: str = Form(None), client_id: str = Form(None), client_secret: str = Form(None)):
    if grant_type != "authorization_code":
        return JSONResponse({"error": "unsupported_grant_type"}, status_code=400)
    try:
        payload = json.loads(base64.urlsafe_b64decode(code.encode()).decode())
    except Exception:
        return JSONResponse({"error": "invalid_code"}, status_code=400)

    now = int(time.time())
    claims = {
        "iss": ISSUER,
        "aud": client_id or CLIENT_ID,
        "sub": payload.get("username", "dev@example.com"),
        "email": payload.get("username", "dev@example.com"),
        "iat": now,
        "exp": now + 3600,
        "roles": payload.get("roles", ["reader"]) 
    }
    id_token = jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALG)
    return {
        "access_token": id_token,
        "id_token": id_token,
        "token_type": "Bearer",
        "expires_in": 3600
    }
