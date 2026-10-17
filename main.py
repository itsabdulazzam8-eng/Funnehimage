from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

# Replace with your actual Webhook URL
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
async def log_request(request: Request):
    # 1. Capture User-Agent to identify the bot
    user_agent = request.headers.get("user-agent", "")
    
    # 2. Identify the visitor IP
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    # 3. BOT FILTERING
    # We now check for the IP start OR the cron-job User-Agent
    bot_ips = ("34.", "35.", "104.", "66.249")
    if client_ip.startswith(bot_ips) or "cron-job.org" in user_agent:
        print(f"DEBUG: Bot ping ignored: {client_ip} | UA: {user_agent}")
        return HTMLResponse(content="<h1>Loading...</h1>")

    print(f"DEBUG: Real visit detected from {client_ip}")

    # 4. Capture metadata
    referrer = request.headers.get("referer", "Direct/None")

    # 5. Lookup location
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
            requests.post(WEBHOOK_URL, json={"content": message}, timeout=5)
    except Exception as e:
        print(f"DEBUG Error: {e}")

    return HTMLResponse(content="<h1>Loading...</h1>")
