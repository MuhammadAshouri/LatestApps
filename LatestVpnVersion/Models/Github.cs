namespace LatestVpnVersion.Models;

public class Github
{
    public string? html_url { get; set; }
    public IList<Asset> assets { get; set; } = new List<Asset>();
}

public class Asset
{
    public string? browser_download_url { get; set; }
    public string? name { get; set; }
}