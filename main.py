# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests, time, hmac, hashlib, json
from urllib.parse import urlencode
import os

app = FastAPI()

# Monta diretório estático
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota raiz serve index.html
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join("static", "index.html"))

# Credenciais Tuya
CLIENT_ID = "y7c8gu59egmduep9tcwh"
CLIENT_SECRET = "aae978c6d8054d058da93364a873ee23"
TUYA_API = "https://openapi.tuyaus.com"


def sha256_hexdigest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def build_string_to_sign(method: str, path: str, query: dict, body: bytes = b"", headers_to_sign: dict = None) -> str:
    query_string = urlencode(sorted(query.items())) if query else ""
    url = path + (f"?{query_string}" if query_string else "")
    content_sha256 = sha256_hexdigest(body)
    optional = ""
    if headers_to_sign:
        optional = "".join(f"{k}:{v}\n" for k, v in headers_to_sign.items())
    return f"{method}\n{content_sha256}\n{optional}\n{url}"


def sign_request(method: str, path: str, query: dict, token: str = "", headers_to_sign: dict = None, body: bytes = b"") -> tuple[str, str]:
    timestamp = str(int(time.time() * 1000))
    string_to_sign = build_string_to_sign(method, path, query, body, headers_to_sign)
    prefix = CLIENT_ID + (token + timestamp if token else timestamp)
    sign = hmac.new(
        CLIENT_SECRET.encode('utf-8'),
        (prefix + string_to_sign).encode('utf-8'),
        hashlib.sha256
    ).hexdigest().upper()
    return sign, timestamp


def get_token() -> str:
    method, path = "GET", "/v1.0/token"
    query = {"grant_type": "1"}
    sign, timestamp = sign_request(method, path, query)
    headers = {
        "client_id": CLIENT_ID,
        "sign": sign,
        "t": timestamp,
        "sign_method": "HMAC-SHA256"
    }
    resp = requests.get(f"{TUYA_API}{path}?grant_type=1", headers=headers)
    data = resp.json()
    if not data.get("success") or "result" not in data:
        raise Exception(f"Failed to get token: {data}")
    return data["result"]["access_token"]


class LampRequest(BaseModel):
    device_ids: list[str]
    color: dict

class PowerRequest(BaseModel):
    device_ids: list[str]
    state: bool

@app.post("/set_color")
def set_color(req: LampRequest):
    token = get_token()
    results = {}
    for did in req.device_ids:
        method, path = "POST", f"/v1.0/devices/{did}/commands"
        # sempre usa saturação e brilho máximos
        val = {"h": req.color.get("h", 0), "s": 1000, "v": 1000}
        body = json.dumps({"commands": [{"code": "colour_data_v2", "value": val}]}).encode('utf-8')
        sign, timestamp = sign_request(method, path, {}, token=token, body=body)
        headers = {
            "client_id": CLIENT_ID,
            "access_token": token,
            "sign": sign,
            "t": timestamp,
            "sign_method": "HMAC-SHA256",
            "Content-Type": "application/json"
        }
        resp = requests.post(f"{TUYA_API}{path}", headers=headers, data=body)
        results[did] = resp.json()
    return {"results": results}

@app.post("/set_power")
def set_power(req: PowerRequest):
    token = get_token()
    results = {}
    for did in req.device_ids:
        method, path = "POST", f"/v1.0/devices/{did}/commands"
        body = json.dumps({"commands": [{"code": "switch_led", "value": req.state}]}).encode('utf-8')
        sign, timestamp = sign_request(method, path, {}, token=token, body=body)
        headers = {
            "client_id": CLIENT_ID,
            "access_token": token,
            "sign": sign,
            "t": timestamp,
            "sign_method": "HMAC-SHA256",
            "Content-Type": "application/json"
        }
        resp = requests.post(f"{TUYA_API}{path}", headers=headers, data=body)
        results[did] = resp.json()
    return {"results": results}

@app.get("/test_connection")
def test_connection():
    token = get_token()
    return {"connection": "ok", "access_token": token}