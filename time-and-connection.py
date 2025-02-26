# Example of partially updating

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
 
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import subprocess

logging.basicConfig(level=logging.DEBUG)

def get_tailscale_status():
    try:
        # Get Tailscale status
        result = subprocess.run(['tailscale', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            return ""
        
        # Extract the relevant line
        status_lines = result.stdout.splitlines()
        status_info = status_lines[0].split()
        ip_address = status_info[0]
        node_name = status_info[1]
        op_system = status_info[3]
        
        if len(status_lines) > 1:
            # Typically, the second line has the active connection info

            return f"{node_name}:{ip_address}"
        else:
            return ""
    
    except Exception as e:
        return f"Tailscale: {e}"

try:
    logging.info("epd2in13_V4 Demo")
    
    epd = epd2in13_V4.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
    wifi_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)

    # showing time and wifi info...
    logging.info("showing time and wifi info...")
    
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    # added to help clear screen. Text was partially drawn previous.
    epd.displayPartial(epd.getbuffer(time_image))

    while True:
        # Get current time string
        time_str = time.strftime('%H:%M')
        # Get current WiFi SSID
        wifi_ssid = os.popen("iwgetid -r").read().strip()
        ip_address = os.popen("hostname -I").read().strip().split(" ")[0]
        tailscale_info = get_tailscale_status()
        if not wifi_ssid:
            wifi_ssid = "No WiFi Connection"
        
        # Clear the entire image
        time_draw.rectangle((0, 0, epd.height, epd.width), fill=255)
        
        # Draw WiFi info in the top left using size 16 font
        time_draw.text((5, 0), wifi_ssid, font=wifi_font, fill=0)
        time_draw.text((5, 17), ip_address, font=wifi_font, fill=0)
        time_draw.text((5, 100), tailscale_info, font=wifi_font, fill=0)
        
        # Use textbbox instead of the deprecated textsize to get text dimensions
        bbox = time_draw.textbbox((0, 0), time_str, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (epd.height - text_width) // 2
        y = ((epd.width - text_height) // 2) - 10
        
        # Draw the centered time
        time_draw.text((x, y), time_str, font=font, fill=0)
        
        # Update display with the new image (partial update)
        epd.displayPartial(epd.getbuffer(time_image))
        time.sleep(60)


    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd.Clear(0xFF)
    logging.info("Goodbye...")
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
