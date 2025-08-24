import flet as ft
import re, os, urllib.parse, random, binascii, uuid, time, secrets, string, requests
from MedoSigner import Argus, Gorgon, Ladon, md5

# نفس دوالك الأصلية لكن بدون تيليجرام بوت
def info(username):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv)"
    }
    try:
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=headers, timeout=10).text
        info = tikinfo.split('webapp.user-detail"')[1].split('"RecommenUserList"')[0]
        id = info.split('id":"')[1].split('",')[0]
        return id
    except:
        return 'h'

def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", sdk_version: int = 2, platform: int = 19, unix: int = None):
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload is not None else None
    if not unix:
        unix = int(time.time())
    return Gorgon(params, unix, payload, cookie).get_value() | {
        "x-ladon": Ladon.encrypt(unix, license_id, aid),
        "x-argus": Argus.get_sign(params, x_ss_stub, unix, platform=platform, aid=aid, license_id=license_id, sec_device_id=sec_device_id, sdk_version=sdk_version_str, sdk_version_int=sdk_version)
    }

def get_level(username):
    id = info(username)
    if id == 'h':
        return 'h'
    url = f"https://webcast16-normal-no1a.tiktokv.eu/webcast/user/?request_from=profile_card_v2&target_uid={id}&iid={random.randint(1, 10**19)}&device_id={random.randint(1, 10**19)}&aid=1233&app_name=musical_ly&version_code=300102&device_platform=android&os=android&cdid={uuid.uuid4()}"

    headers = {
        'User-Agent': "com.zhiliaoapp.musically/2023001020 (Linux; Android 13)"
    }
    headers.update(sign(url.split('?')[1], '', "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233))
    try:
        response = requests.get(url, headers=headers)
        level = re.search(r'"default_pattern":"(.*?)"', response.text).group(1)
        return int(level.split('المستوى رقم ')[1])
    except:
        return 'h'


# تطبيق Flet
def main(page: ft.Page):
    page.title = "TikTok Support Level"
    page.vertical_alignment = "center"

    username_field = ft.TextField(label="TikTok Username", width=300)
    result_text = ft.Text("")

    def check_level(e):
        username = username_field.value.strip().replace("@", "")
        result_text.value = f"Searching for @{username}..."
        page.update()
        level = get_level(username)
        if level != 'h':
            result_text.value = f"🎯 Level: {level}"
        else:
            result_text.value = "❌ لم يتم العثور على معلومات."
        page.update()

    check_btn = ft.ElevatedButton("Check Level", on_click=check_level)

    page.add(
        ft.Column(
            [
                ft.Text("TikTok Broadcast Support Level", size=22, weight="bold"),
                username_field,
                check_btn,
                result_text,
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    )

ft.app(target=main)
