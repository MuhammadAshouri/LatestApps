from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
import requests

from app import app
from config import (V2RAYNG, V2RAYN, CLASH_META, CLASH_VERGE, 
                    NEKOBOX_64, NEKOBOX_32, NEKORAY)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36",
    "Accept": "application/vnd.github+json"
}

def get_download_url(url, keyword, ends=False):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if not json_data:
            raise HTTPException(status_code=404, detail="Not Found")

        assets = json_data.get('assets', [])
        asset = next((c for c in assets if c.get('name') and (ends and c['name'].endswith(keyword) or keyword in c['name'])), None)
        
        if asset and asset.get('browser_download_url'):
            return RedirectResponse(url=asset['browser_download_url'])
        else:
            return RedirectResponse(url=json_data.get('html_url') or url)
    except Exception as ex:
        print(f"Error: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get('/v2rayng')
def get_v2rayng_download():
    return get_download_url(f"https://api.github.com/repos/2dust/v2rayng/releases/{V2RAYNG}", "")

@app.get('/v2rayn')
def get_v2rayn_download():
    return get_download_url(f"https://api.github.com/repos/2dust/v2rayn/releases/{V2RAYN}", "SelfContained")

@app.get('/clash-meta')
def get_clash_meta_download():
    return get_download_url(f"https://api.github.com/repos/MetaCubeX/ClashMetaForAndroid/releases/{CLASH_META}", "universal")

@app.get('/clash-verge')
def get_clash_verge_download():
    return get_download_url(f"https://api.github.com/repos/zzzgydi/clash-verge/releases/{CLASH_VERGE}", "en_US.msi", True)

@app.get('/nekobox-64')
def get_neko_box_arm64_download():
    return get_download_url(f"https://api.github.com/repos/MatsuriDayo/NekoBoxForAndroid/releases/{NEKOBOX_64}", "arm64")

@app.get('/nekobox-32')
def get_neko_box_armeabi_download():
    return get_download_url(f"https://api.github.com/repos/MatsuriDayo/NekoBoxForAndroid/releases/{NEKOBOX_32}", "armeabi")

@app.get('/nekoray')
def get_neko_ray_download():
    return get_download_url(f"https://api.github.com/repos/MatsuriDayo/nekoray/releases/{NEKORAY}", "windows")