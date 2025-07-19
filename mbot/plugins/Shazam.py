from __future__ import unicode_literals
from pyrogram import Client , filters 
from os import environ,execl
from sys import executable
from pyrogram.errors import FloodWait 
from pyrogram.types import Message , InlineKeyboardMarkup, InlineKeyboardButton ,CallbackQuery
from pyrogram.errors import FloodWait 
from asyncio import sleep
from mbot.utils.util import is_maintenance_mode
from mbot import LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot, AUTH_CHATS
from mbot.plugins.music import download_songs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mbot.plugins.lyrics import get_genius_song_id, get_genius_lyrics, LYRIC_RESPONSES
#from database.users_chats_db import db
#from utils import get_size
from shazamio import Shazam
#import math
import asyncio
import time
#import shlex
#import aiofiles
#import aiohttp
import wget
import os
#from asgiref.sync import sync_to_async
from requests import get
from mbot.utils.util import run_cmd as runcmd
import datetime
from json import JSONDecodeError
import requests
#import ffmpeg 
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
#from youtubesearchpython import VideosSearch
import yt_dlp
#from youtube_search import YoutubeSearch
import requests
from typing import Tuple
from pyrogram import filters
from pyrogram import Client
#from mbot import OWNER_ID as ADMINS
import time
from mutagen.id3 import ID3, APIC,error
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from apscheduler.schedulers.background import BackgroundScheduler
from mbot.utils.shazam import humanbytes, edit_or_reply, fetch_audio
from mbot.utils.language_utils import get_user_language
from yt_dlp import YoutubeDL
from pathlib import Path
from lyricsgenius import Genius
from dotenv import load_dotenv
import os
import requests
from yt_dlp import YoutubeDL
from typing import Optional
import os
import re
import requests
from pathlib import Path
from typing import Optional
from yt_dlp import YoutubeDL
load_dotenv()
genius_api = os.getenv('GENIUS_API')  
BAN_LIST_FILE = "banned_users.json"
# Load banned users from file
def load_banned_users():
    if os.path.exists(BAN_LIST_FILE):
        with open(BAN_LIST_FILE, "r") as f:
            return set(json.load(f))
    return set()
banned_users = load_banned_users()
####################################
NOT_SUPPORT = [ ]
ADMINS = 5337964165
COOKIE_PATH = Path("instagram.com_cookies.txt")


@Mbot.on_message(filters.command("test_cookies"))
async def test_cookies(client, message):
    if downloader._check_cookies():  # Use the downloader instance's method
        await message.reply("✅ Cookies working")
    else:
        await message.reply("❌ No valid cookies found")


import os
import random
import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional

COOKIE_PATH = Path("instagram.com_cookies.txt")
COOKIE_REFRESH_INTERVAL = 3600  # 1 hour
MAX_RETRIES = 3
MIN_DELAY = 1
MAX_DELAY = 5

class InstagramDownloader:
    def __init__(self):
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        self.ig_token = os.getenv('INSTAGRAM_TOKEN')
        self.COOKIE_PATH = COOKIE_PATH
        self.last_refresh = 0
        self.refresh_lock = False
        self.methods = [
            self._ytdlp_with_cookies,
            self._third_party_api,
            self._official_api,
            self._ytdlp_direct
        ]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
        self.proxies = self._load_proxies()

    def _load_proxies(self):
        """Load proxies from environment variable"""
        proxy_str = os.getenv('PROXIES', '')
        return [p.strip() for p in proxy_str.split(',') if p.strip()]

    def _get_random_account(self):
        """Get random Instagram account from environment variables"""
        accounts = os.getenv('IG_ACCOUNTS', '').split(',')
        if not accounts or not accounts[0]:
            return os.getenv('IG_USERNAME'), os.getenv('IG_PASSWORD')
        account = random.choice(accounts).strip()
        return account.split(':') if ':' in account else (account, os.getenv('IG_PASSWORD'))

    def _human_type(self, element, text):
        """Simulate human typing with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.3))

    def _get_chrome_options(self):
        """Configure Chrome options to avoid detection"""
        chrome_options = Options()
        
        # Anti-detection settings
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        chrome_options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        
        # Random window size
        chrome_options.add_argument(f"--window-size={random.randint(800,1200)},{random.randint(600,800)}")
        
        # Proxy if available
        if self.proxies and all(':' in p for p in self.proxies):  # Check for valid format
        chrome_options.add_argument(f"--proxy-server={random.choice(self.proxies)}")
        
        # Disable images to speed up
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        return chrome_options

    def refresh_cookies(self):
        """Refresh Instagram cookies with anti-ban measures"""
        if self.refresh_lock:
            raise Exception("Cookie refresh is currently locked")
            
        if time.time() - self.last_refresh < 300:  # 5 min cooldown
            return False
            
        self.refresh_lock = True
        success = False
        
        try:
            for attempt in range(MAX_RETRIES):
                try:
                    username, password = self._get_random_account()
                    if not username or not password:
                        raise ValueError("Instagram credentials not configured")
                    
                    chrome_options = self._get_chrome_options()
                    driver = webdriver.Chrome(options=chrome_options)
                    
                    try:
                        # Mask WebDriver
                        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                            "userAgent": random.choice(self.user_agents)
                        })
                        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                        
                        # Random delay before starting
                        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                        
                        # Open Instagram
                        driver.get("https://www.instagram.com")
                        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                        
                        # Login with human-like behavior
                        username_field = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "username"))
                        )
                        self._human_type(username_field, username)
                        
                        time.sleep(random.uniform(0.5, 1.5))
                        
                        password_field = driver.find_element(By.NAME, "password")
                        self._human_type(password_field, password)
                        
                        time.sleep(random.uniform(0.5, 1.5))
                        
                        # Click login button
                        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                        login_button.click()
                        
                        # Wait for login to complete
                        WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.LINK_TEXT, "Search"))
                        )
                        
                        # Random delay after login
                        time.sleep(random.uniform(3, 7))
                        
                        # Save cookies
                        cookies = driver.get_cookies()
                        with open(self.COOKIE_PATH, 'w') as f:
                            f.write("# Netscape HTTP Cookie File\n")
                            for cookie in cookies:
                                f.write(f"{cookie['domain']}\tTRUE\t{cookie['path']}\tFALSE\t{cookie['expiry']}\t{cookie['name']}\t{cookie['value']}\n")
                        
                        success = True
                        self.last_refresh = time.time()
                        break
                        
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed: {str(e)}")
                        if attempt == MAX_RETRIES - 1:
                            raise
                        time.sleep(random.randint(5, 15))  # Backoff
                        
                    finally:
                        driver.quit()
                        
                except Exception as e:
                    print(f"Cookie refresh failed completely: {str(e)}")
                    raise
                    
        finally:
            self.refresh_lock = False
            
        return success

    def _check_cookies(self):
        """Enhanced cookie validation"""
        if not self.COOKIE_PATH.exists():
            print("⚠️ Cookie file not found")
            return False
            
        # Check file age
        file_age = time.time() - os.path.getmtime(self.COOKIE_PATH)
        if file_age > COOKIE_REFRESH_INTERVAL:
            print(f"⚠️ Cookies expired ({file_age/3600:.1f} hours old)")
            return False
            
        # Check file content
        try:
            with open(self.COOKIE_PATH, 'r') as f:
                content = f.read()
                if "sessionid" not in content:
                    print("⚠️ No sessionid in cookies")
                    return False
        except Exception as e:
            print(f"⚠️ Cookie file read error: {str(e)}")
            return False
            
        print("✅ Cookies are valid")
        return True

    async def download_content(self, url: str) -> Optional[str]:
        """Attempt all download methods with automatic fallback"""
        if not self._validate_instagram_url(url):
            raise ValueError("Invalid Instagram URL format")
            
        # Ensure we have valid cookies
        if not self._check_cookies():
            if not self.refresh_cookies():
                raise Exception("Could not refresh cookies")
            
        last_error = None
        
        for method in self.methods:
            try:
                print(f"Attempting {method.__name__}...")
                if result := await method(url):
                    return result
            except Exception as e:
                last_error = e
                print(f"{method.__name__} failed: {str(e)}")
                continue
        
        print(f"All methods failed. Last error: {last_error}")
        return None

    def _validate_instagram_url(self, url: str) -> bool:
        """Verify URL is a valid Instagram post"""
        patterns = [
            r'https?://(www\.)?instagram\.com/p/',
            r'https?://(www\.)?instagram\.com/reel/',
            r'https?://(www\.)?instagram\.com/tv/'
        ]
        return any(re.search(pattern, url) for pattern in patterns)

    async def _ytdlp_with_cookies(self, url: str) -> Optional[str]:
        """Primary download method using cookies"""
        if not self._check_cookies():
            raise Exception("No valid cookies available")
        
        ydl_opts = {
            'format': 'best',
            'cookiefile': str(self.COOKIE_PATH),
            'outtmpl': '/tmp/ig_cookies_%(id)s.%(ext)s',
            'quiet': True,
            'socket_timeout': 15,
            'extractor_args': {'instagram': {'wait_for_approval': True}}
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        except Exception as e:
            print(f"Cookie method failed: {str(e)}")
            raise

    async def _third_party_api(self, url: str) -> Optional[str]:
        """Fallback to third-party API service"""
        if not self.rapidapi_key:
            raise Exception("RapidAPI key not configured")
            
        headers = {
            'x-rapidapi-key': self.rapidapi_key,
            'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
        }
        
        try:
            res = requests.get(
                "https://instagram-scraper-api2.p.rapidapi.com/v1/media_info",
                headers=headers,
                params={"url": url},
                timeout=15
            )
            res.raise_for_status()
            
            if (video_url := res.json().get('items', [{}])[0].get('video_versions', [{}])[0].get('url')):
                return await self._download_file(video_url, "ig_rapidapi")
        except Exception as e:
            print(f"Third-party API failed: {str(e)}")
            raise
        return None

    async def _official_api(self, url: str) -> Optional[str]:
        """Official Instagram API fallback"""
        if not self.ig_token:
            raise Exception("Instagram token not configured")
            
        try:
            api_url = f"https://graph.facebook.com/v18.0/instagram_oembed?url={url}&access_token={self.ig_token}"
            res = requests.get(api_url, timeout=10)
            res.raise_for_status()
            
            if (thumbnail_url := res.json().get('thumbnail_url')):
                # Get higher quality version if available
                media_url = thumbnail_url.replace('s640x640', 's1080x1080')
                return await self._download_file(media_url, "ig_official")
        except Exception as e:
            print(f"Official API failed: {str(e)}")
            raise
        return None

    async def _ytdlp_direct(self, url: str) -> Optional[str]:
        """Last resort direct download"""
        ydl_opts = {
            'format': 'best',
            'outtmpl': '/tmp/ig_direct_%(id)s.%(ext)s',
            'quiet': True,
            'socket_timeout': 20,
            'extractor_args': {'instagram': {'wait_for_approval': True}}
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        except Exception as e:
            print(f"Direct download failed: {str(e)}")
            raise

    async def _download_file(self, url: str, prefix: str) -> str:
        """Generic file downloader with cleanup"""
        local_path = f"/tmp/{prefix}_{os.urandom(4).hex()}.mp4"
        try:
            with requests.get(url, stream=True, timeout=15) as r:
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_path
        except Exception as e:
            if os.path.exists(local_path):
                os.remove(local_path)
            raise

downloader = InstagramDownloader()

# Schedule periodic cookie refresh
scheduler = BackgroundScheduler()
scheduler.add_job(downloader.refresh_cookies, 'interval', hours=1)
scheduler.start()

# Usage in your handler:
async def handle_instagram_message(message):
    try:
        video_path = await downloader.download_content(message.text)
        if not video_path:
            await message.reply("❌ All download methods failed")
            return None
            
        audio_file = await convert_to_audio(video_path)
        os.remove(video_path)
        return audio_file
        
    except Exception as e:
        await message.reply(f"⚠️ Download error: {str(e)}")
        return None

# Update the shazam_ function to handle Instagram links
# ... (keep all the existing imports and setup code)

@Client.on_message(filters.regex(r'https?://(www\.)?instagram\.com/(p|reel|tv)/'))
async def handle_instagram_links(client, message):
    user_lang = get_user_language(message.from_user.id)
    
    if is_maintenance_mode() and message.from_user.id not in SUDO_USERS:
        await message.reply_text(SHAZ_RESPONSES.get(user_lang, {}).get("maintenance","🔧 The bot is under maintenance. Please try again later."))
        return
    
    if message.from_user.id in banned_users:
        await message.reply_text(SHAZ_RESPONSES.get(user_lang, {}).get("banned","You are banned from using this bot  ദ്ദി ༎ຶ‿༎ຶ ) "))
        return

    stime = time.time()
    sts = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
    msg = await message.reply_text(SHAZ_RESPONSES.get(user_lang, {}).get("processing","Processing Instagram content..."))
    
    try:
        # Download the Instagram video
        video_file = await downloader.download_content(message.text)
        if not video_file:
            return await msg.edit(SHAZ_RESPONSES.get(user_lang, {}).get("invalid_link", "⚠️ Could not download Instagram content. Please try another link."))
        
        # Send the video first
        await message.reply_video(
            video_file,
            caption="Here's the Instagram video you requested",
            reply_to_message_id=message.id
        )
        
        # Convert to audio for Shazam
        music_file = await convert_to_audio(video_file)
        if not music_file:
            return await msg.edit(SHAZ_RESPONSES.get(user_lang, {}).get("Convert_Song", "`Unable To Convert To Song File. Is This A Valid File?`"))
        
        # Shazam the audio
        thumbnail, by, title = await shazam(music_file)
        if not title:
            return await msg.edit(SHAZ_RESPONSES.get(user_lang, {}).get("No_Result", "`No Results Found.`"))
        
        # Download thumbnail if available
        thumb = None
        if thumbnail:
            thumb = wget.download(thumbnail)
        
        # Create inline keyboard with lyrics button
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "Get Lyrics",
                callback_data=f"lyrics_{title}_{by}"
            )]
        ])
        
        etime = time.time()
        t_k = round(etime - stime)
        
        caption = f"""<b><u>Identified Song</b></u>
        
<b>Song Name :</b> <code>{title}</code>
<b>Singer :</b> <code>{by}</code>
<b>Time Taken :</b> <code>{t_k} Seconds</code>

<b><u>Identified By @z_downloadbot</b></u>
"""
        await sts.delete()
        
        # Send the identified song info
        if thumb:
            await msg.delete()
            await message.reply_photo(
                thumb,
                caption=caption,
                quote=True,
                reply_markup=keyboard
            )
        else:
            await msg.edit(
                caption,
                reply_markup=keyboard
            )
        
        # Download and send the full song
        path = await download_songs(title)
        if path:
            audio = EasyID3(path)
            try:
                audio['title'] = title
                audio['artist'] = by
                audio.save()
            except:
                pass
            
            try:
                if thumb:
                    audio = MP3(path, ID3=ID3)
                    audio.tags.add(APIC(
                        mime='image/jpeg',
                        type=3,
                        desc=u'Cover',
                        data=open(thumb,'rb').read()
                    ))
                    audio.save()
            except Exception:
                pass
            
            await message.reply_audio(
                path,
                title=title,
                performer=by,
                caption=f"{title} - {by}",
                thumb=thumb if thumb else None,
                reply_markup=keyboard
            )
            os.remove(path)
        
    except Exception as e:
        await msg.edit(f"⚠️ Error: {str(e)}")
    finally:
        # Clean up files
        if 'video_file' in locals() and video_file and os.path.exists(video_file):
            os.remove(video_file)
        if 'music_file' in locals() and music_file and os.path.exists(music_file):
            os.remove(music_file)
        if 'thumb' in locals() and thumb and os.path.exists(thumb):
            os.remove(thumb)



async def get_lyrics(title, artist, user_id):
    """Fetch lyrics using Genius API only"""
    user_lang = get_user_language(user_id)
    
    # Combine title and artist for better search results
    query = f"{title} {artist}"
    
    try:
        # Get song ID from Genius
        song_id = get_genius_song_id(query)
        if not song_id:
            return LYRIC_RESPONSES.get(user_lang, {}).get("lyrics_not_found", 
                f"Lyrics not found for `{title}` ❌")
        
        # Get lyrics from Genius
        lyrics = get_genius_lyrics(song_id)
        if not lyrics:
            return LYRIC_RESPONSES.get(user_lang, {}).get("lyrics_not_found", 
                f"Lyrics not found for `{title}` ❌")
        
        return lyrics
    
    except Exception as e:
        print(f"Genius lyrics error: {e}")
        return LYRIC_RESPONSES.get(user_lang, {}).get("lyrics_error", 
            "Error fetching lyrics. Please try again later.")

# Modify the lyrics_callback function to pass the user ID
@Client.on_callback_query(filters.regex(r'^lyrics_'))
async def lyrics_callback(client, callback_query):
    user_lang = get_user_language(callback_query.from_user.id)
    
    try:
        _, title, artist = callback_query.data.split('_', 2)
    except ValueError:
        await callback_query.answer(
            LYRIC_RESPONSES.get(user_lang, {}).get("invalid_request", "Invalid request"),
            show_alert=True
        )
        return
    
    await callback_query.answer(LYRIC_RESPONSES.get(user_lang, {}).get("searching", "Searching..."))
    
    try:
        # Pass the user ID to get_lyrics
        lyrics = await get_lyrics(title, artist, callback_query.from_user.id)
        
        # Send as a reply to keep chat clean
        await callback_query.message.reply_text(
            f"<b>{title} - {artist}</b>\n\n{lyrics}",
            reply_to_message_id=callback_query.message.id,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        await callback_query.message.reply_text(
            LYRIC_RESPONSES.get(user_lang, {}).get("lyrics_error", 
            f"Error: {str(e)}"),
            reply_to_message_id=callback_query.message.id
        )
        
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])
#@sync_to_async
def thumb_down(album_id,img):
    with open(f"/tmp/thumbnails/{album_id}.jpg","wb") as file:
        file.write(get(img).content)
    return f"/tmp/thumbnails/{album_id}.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


async def shazam(file):
    shazam = Shazam()
    try:
        r = await shazam.recognize(file)
    except:
        return None, None, None
    if not r:
        return None, None, None
    track = r.get("track")
    nt = track.get("images")
    image = nt.get("coverarthq")
    by = track.get("subtitle")
    title = track.get("title")
    return image, by, title

async def convert_to_audio(vid_path):
    stark_cmd = f"ffmpeg -i {vid_path} -map 0:a friday.mp3"
    await runcmd(stark_cmd)
    final_warner = "friday.mp3"
    if not os.path.exists(final_warner):
        return None
    return final_warner





SHAZ_RESPONSES = {
    "en": {
        "start_download": "🎧 Downloading your request... Please wait!",
        "download_complete": "✅ Download complete! Enjoy your music.",
        "error": "❌ Sorry, an error occurred. Please try again or report this issue.",
        "banned": "🚫 You are banned from using this bot.",
        "maintenance": "🔧 The bot is under maintenance. Please try again later.",
        "invalid_link": "⚠️ Are you sure this is a valid Spotify link?",
        "track_not_found": "⚠️ Track not found. Please try another link.",
        "playlist_info": "▶️ Playlist: {name}\n📝 Description: {description}\n👤 Owner: {owner}\n❤️ Followers: {followers}\n🔢 Total Tracks: {total_tracks}\n\n[IMAGE]({image_url})",
        "album_info": "💽 Album: {name}\n👥 Artists: {artists}\n🎧 Total Tracks: {total_tracks}\n🗂 Category: {album_type}\n📆 Published on: {release_date}\n\n[IMAGE]({image_url})",
        "artist_info": "👤 Artist: {name}\n❤️ Followers: {followers}\n🎶 Genres: {genres}\n🗂 Category: {type}\n❤️ Popularity: {popularity}\n\n[IMAGE]({image_url})",
        "thumbnail_error": "⚠️ Thumbnail download is not available for this track.",
        "preview_error": "⚠️ Audio preview is not available for this track.",
        "Under": "Bot Is Under Maintenance ⚠️",
        "301": "301 Use @y2mate_api_bot Insted Of Me 🚫",
        "417": "417 Not Critical, Retrying Again  🚫",
        "404": "404: sorry, audio preview is not available for this track 😔",
        "sorry": "sorry we removed support of  episode 😔 pls send other types album/playlist/track",
        "telegram says 500": "telegram says 500 error,so please try again later.❣️",
        "Unable To Procced": "Sorry, We Are Unable To Procced It 🤕❣️",
        "Flood_Wait": "Telegram says: [420 FLOOD_WAIT_X] - A wait of {e.value} seconds is required !",
        "Done": "Check out @z_downloadbot(music)  @Zpotify1(News)",
        "Report": 'please report to the dev say "private version" with above  error occurred message',
        "Rights Check": "Dude check weather I have enough rights😎⚠️",
        "title": "🎧 Title",
        "artist": "🎤 Artist",
        "album": "💽 Album",
        "release_year": "🗓 Release Year",
        "image": "IMAGE",
        "track_id": "Track ID",
        "Shazaming": "Shazaming",
        "Reply_Song": "`Reply To Song File`",
        "Reply_Audio": "`Reply To Audio File.`",
        "Convert_Song": "`Unable To Convert To Song File. Is This A Valid File?`",
        "No_Result": "`No Results Found.`"
    },
    "fa": {
        "start_download": "🎧 درخواست شما در حال دانلود... لطفا منتظر بمانید!",
        "download_complete": "✅ دانلود کامل شد! از موسیقی خود لذت ببرید.",
        "error": "❌ متاسفانه خطایی رخ داد. لطفا دوباره امتحان کنید یا مشکل را گزارش دهید.",
        "banned": "🚫 شما از استفاده از این ربات محروم شده‌اید.",
        "maintenance": "🔧 ربات در حال تعمیر و نگهداری است. لطفا بعدا تلاش کنید.",
        "invalid_link": "⚠️ آیا مطمئن هستید که این لینک معتبر است؟",
        "track_not_found": "⚠️ آهنگ پیدا نشد. لطفا لینک دیگری را امتحان کنید.",
        "playlist_info": "▶️ پلی‌لیست: {name}\n📝 توضیحات: {description}\n👤 مالک: {owner}\n❤️ دنبال‌کنندگان: {followers}\n🔢 تعداد آهنگ‌ها: {total_tracks}\n\n[IMAGE]({image_url})",
        "album_info": "💽 آلبوم: {name}\n👥 هنرمندان: {artists}\n🎧 تعداد آهنگ‌ها: {total_tracks}\n🗂 دسته‌بندی: {album_type}\n📆 تاریخ انتشار: {release_date}\n\n[IMAGE]({image_url})",
        "artist_info": "👤 هنرمند: {name}\n❤️ دنبال‌کنندگان: {followers}\n🎶 ژانرها: {genres}\n🗂 دسته‌بندی: {type}\n❤️ محبوبیت: {popularity}\n\n[IMAGE]({image_url})",
        "thumbnail_error": "⚠️ دانلود تصویر برای این آهنگ امکان‌پذیر نیست.",
        "preview_error": "⚠️ پیش‌نمایش صوتی برای این آهنگ موجود نیست.",
        "Under": "ربات در حال تعمیر و نگهداری است ⚠️",
        "301": "301 به جای من از @y2mate_api_bot استفاده کنید 🚫",
        "417": "417 بحرانی نیست، دوباره تلاش می‌کنیم 🚫",
        "404": "404: متاسفانه پیش‌نمایش صوتی برای این آهنگ موجود نیست 😔",
        "sorry": "متاسفانه پشتیبانی از اپیزود حذف شده است 😔 لطفاً انواع دیگر مانند آلبوم/پلی‌لیست/آهنگ ارسال کنید.",
        "telegram says 500": "تلگرام می‌گوید خطای 500، لطفاً بعداً دوباره تلاش کنید.❣️",
        "Unable To Procced": "متاسفانه، ما قادر به پردازش آن نیستیم 🤕❣️",
        "Flood_Wait": "تلگرام می‌گوید: [420 FLOOD_WAIT_X] - نیاز به انتظار {e.value} ثانیه است!",
        "Done": "از @z_downloadbot (موسیقی) و @Zpotify1 (اخبار) دیدن کنید.",
        "Report": 'لطفاً به توسعه‌دهنده گزارش دهید و بگویید "نسخه خصوصی" به همراه پیام خطای بالا.',
        "Rights Check": "دوست، بررسی کن که آیا من به اندازه کافی حقوق دارم 😎⚠️",
        "title": "🎧 عنوان",
        "artist": "🎤 هنرمند",
        "album": "💽 آلبوم",
        "release_year": "🗓 سال انتشار",
        "image": "تصویر",
        "track_id": "شناسه آهنگ",
        "Shazaming": "در حال شناسایی آهنگ",
        "Reply_Song": "`به فایل آهنگ پاسخ دهید`",
        "Reply_Audio": "`به فایل صوتی پاسخ دهید.`",
        "Convert_Song": "`تبدیل به فایل آهنگ امکان‌پذیر نیست. آیا این یک فایل معتبر است؟`",
        "No_Result": "`نتیجه‌ای یافت نشد.`"
    },
    "es": {
        "start_download": "🎧 Descargando tu solicitud... ¡Por favor espera!",
        "download_complete": "✅ ¡Descarga completa! Disfruta de tu música.",
        "error": "❌ Lo siento, ocurrió un error. Inténtalo de nuevo o informa del problema.",
        "banned": "🚫 Estás prohibido de usar este bot.",
        "maintenance": "🔧 El bot está en mantenimiento. Inténtalo más tarde.",
        "invalid_link": "⚠️ ¿Estás seguro de que este enlace de Spotify es válido?",
        "track_not_found": "⚠️ Pista no encontrada. Intenta con otro enlace.",
        "playlist_info": "▶️ Lista de reproducción: {name}\n📝 Descripción: {description}\n👤 Propietario: {owner}\n❤️ Seguidores: {followers}\n🔢 Total de pistas: {total_tracks}\n\n[IMAGE]({image_url})",
        "album_info": "💽 Álbum: {name}\n👥 Artistas: {artists}\n🎧 Total de pistas: {total_tracks}\n🗂 Categoría: {album_type}\n📆 Publicado el: {release_date}\n\n[IMAGE]({image_url})",
        "artist_info": "👤 Artista: {name}\n❤️ Seguidores: {followers}\n🎶 Géneros: {genres}\n🗂 Categoría: {type}\n❤️ Popularidad: {popularity}\n\n[IMAGE]({image_url})",
        "thumbnail_error": "⚠️ No se puede descargar la miniatura de esta pista.",
        "preview_error": "⚠️ La vista previa de audio no está disponible para esta pista.",
        "Under": "El bot está en mantenimiento ⚠️",
        "301": "301 Usa @y2mate_api_bot en lugar de mí �",
        "417": "417 No es crítico, reintentando de nuevo 🚫",
        "404": "404: Lo siento, la vista previa de audio no está disponible para esta pista 😔",
        "sorry": "Lo siento, eliminamos el soporte para episodios 😔 Por favor, envía otros tipos como álbum/lista de reproducción/pista.",
        "telegram says 500": "Telegram dice error 500, por favor, inténtalo de nuevo más tarde.❣️",
        "Unable To Procced": "Lo siento, no podemos procesarlo 🤕❣️",
        "Flood_Wait": "Telegram dice: [420 FLOOD_WAIT_X] - Se requiere una espera de {e.value} segundos.",
        "Done": "Echa un vistazo a @z_downloadbot (música) y @Zpotify1 (noticias).",
        "Report": 'Por favor, informa al desarrollador diciendo "versión privada" con el mensaje de error anterior.',
        "Rights Check": "Amigo, verifica si tengo suficientes derechos 😎⚠️",
        "title": "🎧 Título",
        "artist": "🎤 Artista",
        "album": "💽 Álbum",
        "release_year": "🗓 Año de lanzamiento",
        "image": "IMAGEN",
        "track_id": "ID de pista",
        "Shazaming": "Identificando canción",
        "Reply_Song": "`Responder al archivo de canción`",
        "Reply_Audio": "`Responder al archivo de audio.`",
        "Convert_Song": "`No se puede convertir a archivo de canción. ¿Es este un archivo válido?`",
        "No_Result": "`No se encontraron resultados.`"
        
    },
    "ru": {
        "start_download": "🎧 Загружается ваш запрос... Пожалуйста, подождите!",
        "download_complete": "✅ Загрузка завершена! Наслаждайтесь вашей музыкой.",
        "error": "❌ Извините, произошла ошибка. Попробуйте еще раз или сообщите о проблеме.",
        "banned": "🚫 Вам запрещено использовать этого бота.",
        "maintenance": "🔧 Бот на техническом обслуживании. Попробуйте позже.",
        "invalid_link": "⚠️ Вы уверены, что это действительная ссылка на Spotify?",
        "track_not_found": "⚠️ Трек не найден. Попробуйте другую ссылку.",
        "playlist_info": "▶️ Плейлист: {name}\n📝 Описание: {description}\n👤 Владелец: {owner}\n❤️ Подписчики: {followers}\n🔢 Всего треков: {total_tracks}\n\n[IMAGE]({image_url})",
        "album_info": "💽 Альбом: {name}\n👥 Исполнители: {artists}\n🎧 Всего треков: {total_tracks}\n🗂 Категория: {album_type}\n📆 Дата выхода: {release_date}\n\n[IMAGE]({image_url})",
        "artist_info": "👤 Исполнитель: {name}\n❤️ Подписчики: {followers}\n🎶 Жанры: {genres}\n🗂 Категория: {type}\n❤️ Популярность: {popularity}\n\n[IMAGE]({image_url})",
        "thumbnail_error": "⚠️ Миниатюра для этого трека недоступна.",
        "preview_error": "⚠️ Аудио-превью для этого трека недоступно.",
        "Under": "Бот на техническом обслуживании ⚠️",
        "301": "301 Используйте @y2mate_api_bot вместо меня 🚫",
        "417": "417 Не критично, пробуем снова 🚫",
        "404": "404: Извините, аудио-превью для этого трека недоступно 😔",
        "sorry": "Извините, поддержка эпизодов удалена 😔 Пожалуйста, отправьте другие типы, такие как альбом/плейлист/трек.",
        "telegram says 500": "Telegram сообщает об ошибке 500, пожалуйста, попробуйте позже.❣️",
        "Unable To Procced": "Извините, мы не можем обработать это 🤕❣️",
        "Flood_Wait": "Telegram сообщает: [420 FLOOD_WAIT_X] - Требуется ожидание {e.value} секунд!",
        "Done": "Проверьте @z_downloadbot (музыка) и @Zpotify1 (новости).",
        "Report": 'Пожалуйста, сообщите разработчику, сказав "частная версия" с сообщением об ошибке выше.',
        "Rights Check": "Чувак, проверь, есть ли у меня достаточно прав 😎⚠️",
        "title": "🎧 Название",
        "artist": "🎤 Исполнитель",
        "album": "💽 Альбом",
        "release_year": "🗓 Год выпуска",
        "image": "ИЗОБРАЖЕНИЕ",
        "track_id": "ID трека",
        "Shazaming": "Идентификация песни",
        "Reply_Song": "`Ответить на файл песни`",
        "Reply_Audio": "`Ответить на аудиофайл.`",
        "Convert_Song": "`Невозможно преобразовать в файл песни. Это действительный файл?`",
        "No_Result": "`Результаты не найдены.`",
        "Shazaming": "Identificando canción",
        "Reply_Song": "`Responder al archivo de canción`",
        "Reply_Audio": "`Responder al archivo de audio.`",
        "Convert_Song": "`No se puede convertir a archivo de canción. ¿Es este un archivo válido?`",
        "No_Result": "`No se encontraron resultados.`"
    },
    "ar": {
        "start_download": "🎧 يتم تنزيل طلبك... يرجى الانتظار!",
        "download_complete": "✅ تم اكتمال التنزيل! استمتع بموسيقاك.",
        "error": "❌ عذرًا، حدث خطأ. يرجى المحاولة مرة أخرى أو الإبلاغ عن المشكلة.",
        "banned": "🚫 أنت محظور من استخدام هذا البوت.",
        "maintenance": "🔧 البوت تحت الصيانة. يرجى المحاولة لاحقًا.",
        "invalid_link": "⚠️ هل أنت متأكد أن هذا رابط سبوتيفاي صالح؟",
        "track_not_found": "⚠️ لم يتم العثور على المسار. يرجى تجربة رابط آخر.",
        "playlist_info": "▶️ قائمة التشغيل: {name}\n📝 الوصف: {description}\n👤 المالك: {owner}\n❤️ المتابعون: {followers}\n🔢 إجمالي المسارات: {total_tracks}\n\n[IMAGE]({image_url})",
        "album_info": "💽 الألبوم: {name}\n👥 الفنانون: {artists}\n🎧 إجمالي المسارات: {total_tracks}\n🗂 الفئة: {album_type}\n📆 تاريخ الإصدار: {release_date}\n\n[IMAGE]({image_url})",
        "artist_info": "👤 الفنان: {name}\n❤️ المتابعون: {followers}\n🎶 الأنواع: {genres}\n🗂 الفئة: {type}\n❤️ الشعبية: {popularity}\n\n[IMAGE]({image_url})",
        "thumbnail_error": "⚠️ لا يمكن تنزيل الصورة المصغرة لهذا المسار.",
        "preview_error": "⚠️ المعاينة الصوتية غير متاحة لهذا المسار.",
        "Under": "البوت تحت الصيانة ⚠️",
        "301": "301 استخدم @y2mate_api_bot بدلاً مني 🚫",
        "417": "417 ليس حرجًا، يتم إعادة المحاولة مرة أخرى 🚫",
        "404": "404: عذرًا، المعاينة الصوتية غير متاحة لهذا المسار 😔",
        "sorry": "عذرًا، لقد أزلنا دعم الحلقات 😔 يرجى إرسال أنواع أخرى مثل الألبوم/قائمة التشغيل/المسار.",
        "telegram says 500": "Telegram يقول خطأ 500، يرجى المحاولة مرة أخرى لاحقًا.❣️",
        "Unable To Procced": "عذرًا، لا يمكننا معالجة ذلك 🤕❣️",
        "Flood_Wait": "Telegram يقول: [420 FLOOD_WAIT_X] - يلزم انتظار {e.value} ثانية!",
        "Done": "تحقق من @z_downloadbot (موسيقى) و @Zpotify1 (أخبار).",
        "Report": 'يرجى الإبلاغ إلى المطور بقول "نسخة خاصة" مع رسالة الخطأ أعلاه.',
        "Rights Check": "يا صديقي، تحقق مما إذا كان لدي الصلاحيات الكافية 😎⚠️",
        "title": "🎧 العنوان",
        "artist": "🎤 الفنان",
        "album": "💽 الألبوم",
        "release_year": "🗓 سنة الإصدار",
        "image": "صورة",
        "track_id": "معرف المسار",
        "Shazaming": "جاري التعرف على الأغنية",
        "Reply_Song": "`الرد على ملف الأغنية`",
        "Reply_Audio": "`الرد على ملف الصوت.`",
        "Convert_Song": "`تعذر التحويل إلى ملف أغنية. هل هذا ملف صالح؟`",
        "No_Result": "`لم يتم العثور على نتائج.`"
    },
    "hi": {
        "start_download": "🎧 आपका अनुरोध डाउनलोड हो रहा है... कृपया प्रतीक्षा करें!",
        "download_complete": "✅ डाउनलोड पूरा हुआ! अपने संगीत का आनंद लें।",
        "error": "❌ क्षमा करें, एक त्रुटि हुई। कृपया पुनः प्रयास करें या इस समस्या की रिपोर्ट करें।",
        "banned": "🚫 आपको इस बॉट के उपयोग से प्रतिबंधित किया गया है।",
        "maintenance": "🔧 बॉट का रखरखाव किया जा रहा है। कृपया बाद में प्रयास करें।",
        "invalid_link": "⚠️ क्या आपको यकीन है कि यह एक मान्य स्पॉटीफाई लिंक है?",
        "track_not_found": "⚠️ ट्रैक नहीं मिला। कृपया किसी अन्य लिंक का प्रयास करें।",
        "playlist_info": "▶️ प्लेलिस्ट: {name}\n📝 विवरण: {description}\n👤 मालिक: {owner}\n❤️ अनुयायी: {followers}\n🔢 कुल ट्रैक: {total_tracks}\n\n[IMAGE]({image_url})",
        "album_info": "💽 एल्बम: {name}\n👥 कलाकार: {artists}\n🎧 कुल ट्रैक: {total_tracks}\n🗂 श्रेणी: {album_type}\n📆 प्रकाशित तिथि: {release_date}\n\n[IMAGE]({image_url})",
        "artist_info": "👤 कलाकार: {name}\n❤️ अनुयायी: {followers}\n🎶 शैलियाँ: {genres}\n🗂 श्रेणी: {type}\n❤️ लोकप्रियता: {popularity}\n\n[IMAGE]({image_url})",
        "thumbnail_error": "⚠️ इस ट्रैक के लिए थंबनेल डाउनलोड उपलब्ध नहीं है।",
        "preview_error": "⚠️ इस ट्रैक के लिए ऑडियो पूर्वावलोकन उपलब्ध नहीं है।",
        "Under": "बॉट का रखरखाव चल रहा है ⚠️",
        "301": "301 मेरे बजाय @y2mate_api_bot का उपयोग करें 🚫",
        "417": "417 गंभीर नहीं है, फिर से प्रयास कर रहे हैं 🚫",
        "404": "404: क्षमा करें, इस ट्रैक के लिए ऑडियो पूर्वावलोकन उपलब्ध नहीं है 😔",
        "sorry": "क्षमा करें, हमने एपिसोड का समर्थन हटा दिया है 😔 कृपया अन्य प्रकार जैसे एल्बम/प्लेलिस्ट/ट्रैक भेजें।",
        "telegram says 500": "Telegram कहता है 500 त्रुटि, कृपया बाद में पुनः प्रयास करें।❣️",
        "Unable To Procced": "क्षमा करें, हम इसे संसाधित करने में असमर्थ हैं 🤕❣️",
        "Flood_Wait": "Telegram कहता है: [420 FLOOD_WAIT_X] - {e.value} सेकंड की प्रतीक्षा आवश्यक है!",
        "Done": "@z_downloadbot (संगीत) और @Zpotify1 (समाचार) देखें।",
        "Report": 'कृपया डेवलपर को "निजी संस्करण" कहकर और ऊपर की त्रुटि संदेश के साथ रिपोर्ट करें।',
        "Rights Check": "यार, जांचें कि क्या मेरे पास पर्याप्त अधिकार हैं 😎⚠️",
        "title": "🎧 शीर्षक",
        "artist": "🎤 कलाकार",
        "album": "💽 एल्बम",
        "release_year": "🗓 रिलीज़ वर्ष",
        "image": "छवि",
        "track_id": "ट्रैक आईडी",
        "Shazaming": "गाना पहचाना जा रहा है",
        "Reply_Song": "`गाने की फ़ाइल का जवाब दें`",
        "Reply_Audio": "`ऑडियो फ़ाइल का जवाब दें।`",
        "Convert_Song": "`गाने की फ़ाइल में बदलने में असमर्थ। क्या यह एक वैध फ़ाइल है?`",
        "No_Result": "`कोई परिणाम नहीं मिला।`"
    },
}

LANGUAGE_STRINGS = {
    "en": {  # English
        "title": "🎧 Title",
        "artist": "🎤 Artist",
        "album": "💽 Album",
        "release_year": "🗓 Release Year",
        "image": "IMAGE",
        "track_id": "Track ID",
        "track_not_found": "Track Not Found ⚠️",
        "playlist": "Playlist",
        "description": "Description",
        "owner": "Owner",
        "followers": "Followers",
        "total_tracks": "Total Tracks",
        "valid_playlist_question": "Are you sure it's a valid playlist? 🤨",
        "valid_song_question": "are you sure it's a valid song 🤨?"

    },
    "fa": {  # Persian (Farsi)
        "title": "🎧 عنوان",
        "artist": "🎤 هنرمند",
        "album": "💽 آلبوم",
        "release_year": "🗓 سال انتشار",
        "image": "تصویر",
        "track_id": "شناسه آهنگ",
        "track_not_found": "آهنگ پیدا نشد ⚠️",
        "playlist": "لیست پخش",
        "description": "توضیحات",
        "owner": "مالک",
        "followers": "دنبال کنندگان",
        "total_tracks": "تعداد ترک‌ها",
        "valid_playlist_question": "آیا مطمئن هستید که این یک لیست پخش معتبر است؟ 🤨",
        "valid_song_question": "آیا مطمئن هستید که آهنگ معتبری است؟ 🤨"
    },
    "es": {  # Spanish
        "title": "🎧 Título",
        "artist": "🎤 Artista",
        "album": "💽 Álbum",
        "release_year": "🗓 Año de lanzamiento",
        "image": "IMAGEN",
        "track_id": "ID de pista",
        "track_not_found": "Pista no encontrada ⚠️",
        "playlist": "Lista de reproducción",
        "description": "Descripción",
        "owner": "Propietario",
        "followers": "Seguidores",
        "total_tracks": "Total de pistas",
        "valid_playlist_question": "¿Estás seguro de que es una lista de reproducción válida? 🤨",
        "valid_song_question": "¿Estás segura de que es una canción válida 🤨?"

    },
    "ru": {  # Russian
        "title": "🎧 Название",
        "artist": "🎤 Исполнитель",
        "album": "💽 Альбом",
        "release_year": "🗓 Год выпуска",
        "image": "ИЗОБРАЖЕНИЕ",
        "track_id": "ID трека",
        "track_not_found": "Трек не найден ⚠️",
        "playlist": "Плейлист",
        "description": "Описание",
        "owner": "Владелец",
        "followers": "Подписчики",
        "total_tracks": "Всего треков",
        "valid_playlist_question": "¿Я уверен, что список воспроизведений действителен? 🤨",
        "valid_song_question": "вы уверены, что это допустимая песня 🤨?"
    },
    "ar": {  # Arabic
        "title": "🎧 العنوان",
        "artist": "🎤 الفنان",
        "album": "💽 الألبوم",
        "release_year": "🗓 سنة الإصدار",
        "image": "صورة",
        "track_id": "معرف المسار",
        "track_not_found": "لم يتم العثور على المسار ⚠️",
        "playlist": "قائمة تشغيل",
        "description": "الوصف",
        "owner": "المالك",
        "followers": "المتابعون",
        "total_tracks": "إجمالي المسارات",
        "valid_playlist_question": "هل من المؤكد أنها قائمة إعادة إنتاج صالحة؟ 🤨",
        "valid_song_question": "هل أنت متأكد من أن هذه أغنية صالحة 🤨؟"

    },
    "hi": {  # Hindi
        "title": "🎧 शीर्षक",
        "artist": "🎤 कलाकार",
        "album": "💽 एल्बम",
        "release_year": "🗓 रिलीज़ वर्ष",
        "image": "छवि",
        "track_id": "ट्रैक आईडी",
        "track_not_found": "ट्रैक नहीं मिला ⚠️",
        "playlist": "प्लेलिस्ट",
        "description": "विवरण",
        "owner": "मालिक",
        "followers": "फॉलोअर्स",
        "total_tracks": "कुल गाने",
        "valid_playlist_question": "¿क्या आप वैध पुनरुत्पादन सूची तैयार कर सकते हैं? 🤨",
        "valid_song_question": "क्या आप सुनिश्चित हैं कि यह एक वैध गीत है 🤨?"
    }
}