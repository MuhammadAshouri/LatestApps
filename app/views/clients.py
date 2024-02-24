from fastapi import HTTPException
from fastapi.responses import RedirectResponse
import requests
import json

from app import app, logger
from config import VERSIONS_JSON


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36",
    "Accept": "application/vnd.github+json"
}


@app.get('/versions')
def get_saved_versions():
    try:
        with open(VERSIONS_JSON, "r") as json_file:
            versions_data = json.load(json_file)
        return versions_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Versions not found")


def get_download_url(url, keywords, ends=False):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()

        if not json_data:
            raise HTTPException(status_code=404, detail="Not Found")

        assets = json_data.get('assets', [])
        asset = next((c for c in assets if c.get('name') and (ends and c['name'].endswith(tuple(keywords)) or any(keyword in c['name'] for keyword in keywords))), None)

        if not asset :
            raise HTTPException(status_code=404, detail="Couldn't Find This Version Of App.")

        if asset and asset.get('browser_download_url'):
            return RedirectResponse(url=asset['browser_download_url'])
        else:
            return RedirectResponse(url=json_data.get('html_url') or url)
    except Exception as ex:
        logger.error(f"Error: {str(ex)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get('/{client_type}/{version}')
def get_client_download(client_type: str, version: str = "latest"):

    url = f"https://api.github.com/repos/{get_repo_name(client_type)}/releases/{version}"

    if client_type == "v2rayng":
        return get_download_url(url)
    elif client_type == "v2rayn":
        return get_download_url(url, ["SelfContained"])
    elif client_type == "clash_meta":
        return get_download_url(url, ["universal"])
    elif client_type == "clash_verge":
        return get_download_url(url, ["en_US.msi"], True)
    elif client_type == "nekobox_64":
        return get_download_url(url, ["arm64"])
    elif client_type == "nekobox_32":
        return get_download_url(url, ["armeabi"])
    elif client_type == "nekoray":
        return get_download_url(url, ["windows"])
    elif client_type == "singbox":
        return get_download_url(url, ["SFA", "universal"])
    else:
        raise HTTPException(status_code=404, detail="Client not found")


def get_repo_name(client_type: str):
    try:
        return repo_mapping.get(client_type, "")
    except Exception:
        raise HTTPException(status_code=404, detail="Client not found")


repo_mapping = {
        "v2rayng": "2dust/v2rayng",
        "v2rayn": "2dust/v2rayn",
        "clash_meta": "MetaCubeX/ClashMetaForAndroid",
        "clash_verge": "zzzgydi/clash-verge",
        "nekobox_64": "MatsuriDayo/NekoBoxForAndroid",
        "nekobox_32": "MatsuriDayo/NekoBoxForAndroid",
        "nekoray": "MatsuriDayo/nekoray",
        "singbox":"SagerNet/sing-box"
    }
