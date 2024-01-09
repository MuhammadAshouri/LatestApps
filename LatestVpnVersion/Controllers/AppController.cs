using LatestVpnVersion.Models;

namespace LatestVpnVersion.Controllers;

using Microsoft.AspNetCore.Mvc;
using System;
using System.Net.Http;
using System.Threading.Tasks;

[ApiController]
public class AppController : ControllerBase
{
    private readonly HttpClient HttpClient;

    public AppController()
    {
        HttpClient = new HttpClient();
        HttpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36");
        HttpClient.DefaultRequestHeaders.Add("Accept", "application/vnd.github+json");
    }

    [HttpGet("v2rayng")]
    public async Task<IActionResult> GetV2RayNgDownload() =>
        await GetDownloadUrl("https://api.github.com/repos/2dust/v2rayng/releases/latest", "");

    [HttpGet("v2rayn")]
    public async Task<IActionResult> GetV2RayNDownload() =>
        await GetDownloadUrl("https://api.github.com/repos/2dust/v2rayn/releases/latest", "SelfContained");

    [HttpGet("clash-meta")]
    public async Task<IActionResult> GetClashMetaDownload() =>
        await GetDownloadUrl("https://api.github.com/repos/MetaCubeX/ClashMetaForAndroid/releases/latest", "universal");

    [HttpGet("nekobox-64")]
    public async Task<IActionResult> GetNekoBoxArm64Download() =>
        await GetDownloadUrl("https://api.github.com/repos/MatsuriDayo/NekoBoxForAndroid/releases/latest", "arm64");

    [HttpGet("nekobox-32")]
    public async Task<IActionResult> GetNekoBoxArmeabiDownload() =>
        await GetDownloadUrl("https://api.github.com/repos/MatsuriDayo/NekoBoxForAndroid/releases/latest", "armeabi");

    [HttpGet("clash-verge")]
    public async Task<IActionResult> GetClashVergeDownload() =>
        await GetDownloadUrl("https://api.github.com/repos/zzzgydi/clash-verge/releases/latest", "en_US.msi", true);

    [HttpGet("nekoray")]
    public async Task<IActionResult> GetNekoRayDownload() =>
        await GetDownloadUrl("https://api.github.com/repos/MatsuriDayo/nekoray/releases/latest", "windows");

    private async Task<IActionResult> GetDownloadUrl(string url, string keyword, bool ends = false)
    {
        try
        {
            var json = await HttpClient.GetFromJsonAsync<Github>(url);
            if (json == null) return Redirect(url);

            var asset = json.assets.FirstOrDefault(c => c.name != null && (ends ? c.name.EndsWith(keyword) : c.name.Contains(keyword)));
            return asset?.browser_download_url == null ? Redirect(json.html_url ?? url) : Redirect(asset.browser_download_url);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            return StatusCode(500, "Internal server error");
        }
    }
}