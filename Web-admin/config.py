import os 
# Flask configuration
DEBUG = True
SECRET_KEY = 'ALPHA'

# Web admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'  # Change this in production
TELEGRAM_TOKEN = '7688318906:AAF2wCe6hE4Dp5yIDh0WU6rQxYvSDtI0tHQ' # Add your bot token to config.py

# Bot paths 
BOT_PATH = '/home/zaco/zpotify1'  # Update this with your bot's path
LOG_FILE = os.path.join(BOT_PATH, 'bot.log')