import requests
import json

from app import logger, scheduler
from config import VERSIONS_JSON


def get_versions(repo_url):

    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        releases = response.json()

        versions = [(t["tag_name"]) for t in releases]
        logger.info(f"Fetched versions for {repo_url}: {versions}")

        return versions
    except Exception as ex:
        logger.error(f"Failed to fetch releases for {repo_url}. Error: {str(ex)}")
        return None


def save_versions():
    versions_data = {}
    for client_type, repo_name in repo_mapping.items():
        repo_url = f"https://api.github.com/repos/{repo_name}/releases?per_page=100"
        versions = get_versions(repo_url)
        versions_data[client_type] = versions


    with open(VERSIONS_JSON, "w") as json_file:
        json.dump(versions_data, json_file, indent=4)


repo_mapping = {
        "v2rayng": "2dust/v2rayNG",
        "v2rayn": "2dust/v2rayn",
        "clash_meta": "MetaCubeX/ClashMetaForAndroid",
        "clash_verge": "zzzgydi/clash-verge",
        "nekobox": "MatsuriDayo/NekoBoxForAndroid",
        "nekoray": "MatsuriDayo/nekoray",
        "singbox":"SagerNet/sing-box"
    }


scheduler.add_job(save_versions, 'interval', hours=1, coalesce=True, max_instances=1)