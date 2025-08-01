from pyrogram import Client, filters , __version__
from modules.plugins_1system.uptime import bot_start_time
from command import fox_command
import os
import subprocess
from platform import python_version, system, release , uname
import configparser
from pathlib import Path
from datetime import datetime



# Default
DEFAULT_INFO_IMAGE = "https://raw.githubusercontent.com/FoxUserbot/FoxUserbot/refs/heads/main/photos/system_info.jpg"
THEME_PATH = "userdata/theme.ini"



def get_platform_info():
    os_name = system()
    os_release = release()
    termux_vars = [
        'TERMUX_VERSION',
        'TERMUX_APK_RELEASE',
        'PREFIX',
    ]
    if any(var in os.environ for var in termux_vars):
        return '<emoji id="5409357944619802453">📱</emoji> Termux'
    
    if "microsoft-standard" in uname().release:
        return '<emoji id="6298333093044422573">😥</emoji> WSL'
    if "SHARKHOST" in os.environ or "sharkhost" in subprocess.check_output("cat /etc/hostname", shell=True, text=True).strip():
        return '<emoji id="5361632650278744629">🦈</emoji> SharkHost'
    if "DOCKER" in os.environ:
        return '<emoji id="5301137237050663843">👩‍💻</emoji> Docker'
    os_names = {
        'Linux': '<emoji id="5300957668762987048">👩‍💻</emoji> Linux',
        'Windows': '<emoji id="5366318141771096216">👩‍💻</emoji> Windows', 
        'Darwin': '<emoji id="5301155675345265040">👩‍💻</emoji> macOS',
    }
    try:
        os_display = os_names.get(os_name, f'💻 {os_name}')
        return f"{os_display} ({os_release})"
    except:
        return f"💻 {os_name} ({os_release})"


def format_uptime():
    uptime = datetime.now() - bot_start_time()
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    result = []
    if days > 0:
        result.append(f"{days} days")
    if hours > 0:
        result.append(f"{hours} hours")
    if minutes > 0:
        result.append(f"{minutes} minutes")
    if not result:
        result.append(f"{seconds} seconds")
    
    return ' '.join(result)


def replace_aliases(text, message):
    uptime_text = format_uptime()
    platform_text = get_platform_info()
    
    aliases = {
        '{version}': __version__,
        '{python_version}': python_version(),
        '{uptime}': uptime_text,
        '{platform}': platform_text,
    }
    

    for alias, value in aliases.items():
        text = text.replace(alias, str(value))

    if message.from_user.is_premium:
        footer = f"""
<blockquote expandable><emoji id="5330237710655306682">📱</emoji><a href="https://t.me/foxteam0"><b> | Official FoxTeam Channel.</b></a>
<emoji id="5346181118884331907">📱</emoji><a href="https://github.com/FoxUserbot/FoxUserbot"><b> | Github Repository.</b></a>
<emoji id="5379999674193172777">🔭</emoji><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install"><b> | Installation Guide.</b></a></blockquote>
    """
    else:
        footer = f"""
<blockquote expandable><b><a href="https://t.me/foxteam0">💻 | Official FoxTeam Channel.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot">🐈‍⬛ | Github Repository.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install">🤔 | Installation Guide.</a></b></blockquote>
"""
    return text + footer


def get_info_image():
    if not Path(THEME_PATH).exists():
        return DEFAULT_INFO_IMAGE

    try:
        config = configparser.ConfigParser()
        config.read(THEME_PATH)
        return config.get("info", "image", fallback=DEFAULT_INFO_IMAGE)
    except:
        return DEFAULT_INFO_IMAGE




def get_info_text(message):
    uptime_text = format_uptime()
    platform_text = get_platform_info()
    
    custom_text = None
    if Path(THEME_PATH).exists():
        try:
            config = configparser.ConfigParser()
            config.read(THEME_PATH)
            custom_text = config.get("info", "text", fallback=None)
            if custom_text and custom_text.strip() and custom_text != "Not set":
                return replace_aliases(custom_text, message)
        except Exception as e:
            pass
    
    if message.from_user.is_premium:
        return f"""
<emoji id="5190875290439525089">😊</emoji><b> | FoxUserbot INFO</b>
<emoji id="5372878077250519677">📱</emoji><b> | Python: {python_version()}</b>
<emoji id="5190637731503415052">🦊</emoji><b> | Kurigram: {__version__}</b>
<emoji id="5282843764451195532">🖥</emoji><b> | Uptime: {uptime_text}</b>
<emoji id="5350554349074391003">💻</emoji><b> | Platform: {platform_text}</b>
    
<emoji id="5330237710655306682">📱</emoji><a href="https://t.me/foxteam0"><b> | Official FoxTeam Channel.</b></a>
<emoji id="5346181118884331907">📱</emoji><a href="https://github.com/FoxUserbot/FoxUserbot"><b> | Github Repository.</b></a>
<emoji id="5379999674193172777">🔭</emoji><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install"><b> | Installation Guide.</b></a>
    
<emoji id=5350554349074391003>💻</emoji> | <b>Developers:</b>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/a9_fm">A9FM</a>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/ArThirtyFour">ArThirtyFour</a>

<emoji id="5359480394922082925">📱</emoji> | <b>Designer:</b>
<emoji id="5330237710655306682">📱</emoji> | <a href="https://t.me/nw_off">Nw_Off</a>
    """
    else:
        return f"""
<b>🦊 | FoxUserbot INFO</b>
<b>🐍 | Python: {python_version()}</b>
<b>🥧 | Kurigram: {__version__}</b>
<b>⏰ | Uptime: {uptime_text}</b>
<b>💻 | Platform: {platform_text}</b>

<b><a href="https://t.me/foxteam0">💻 | Official FoxTeam Channel.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot">🐈‍⬛ | Github Repository.</a></b>
<b><a href="https://github.com/FoxUserbot/FoxUserbot#how-to-install">🤔 | Installation Guide.</a></b>

💻 | <b>Developers:</b>
📞 | <a href="https://t.me/a9_fm">A9FM</a>
📞 | <a href="https://t.me/ArThirtyFour">ArThirtyFour</a>

🖼 | <b>Designer:</b>
📞 | <a href="https://t.me/nw_off">Nw_Off</a>
    """


@Client.on_message(fox_command("info", "Info", os.path.basename(__file__)) & filters.me)
async def info(client, message):
    try:
        media_url = get_info_image()
        info_text = get_info_text(message)
        file_extension = media_url.split(".")[-1]
        if file_extension in ["mp4", "mov", "avi", "mkv", "webm"]:
            await client.send_video(
                message.chat.id, 
                video=media_url, 
                caption=info_text,
                message_thread_id=message.message_thread_id
            )
        elif file_extension == "gif":
            await client.send_animation(
                message.chat.id, 
                animation=media_url, 
                caption=info_text,
                message_thread_id=message.message_thread_id
            )
        else:           
            await client.send_photo(
                message.chat.id, 
                photo=media_url, 
                caption=info_text,
                message_thread_id=message.message_thread_id
            )
        await message.delete()
    except Exception as e:
        print(f"Error: {e}")
        try:
            await client.send_photo(
                message.chat.id, 
                photo=DEFAULT_INFO_IMAGE, 
                caption=get_info_text(message), 
                message_thread_id=message.message_thread_id
            )
        except:
            try:
                await client.send_photo(
                    message.chat.id, 
                    photo="photos/system_info.jpg", 
                    caption=get_info_text(message), 
                    message_thread_id=message.message_thread_id
                )
            except:
                await message.edit(get_info_text(message))
