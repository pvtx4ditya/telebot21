import requests
import pyshorteners

s = pyshorteners.Shortener()


def download_terabox_video(url, shorturl, password=None):
  headers = {
      'accept':
      '*/*',
      'accept-language':
      'en-GB,en;q=0.9',
      'referer':
      'https://terabox.hnn.workers.dev/',
      'sec-ch-ua':
      '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
      'sec-ch-ua-mobile':
      '?0',
      'sec-ch-ua-platform':
      '"Windows"',
      'sec-fetch-dest':
      'empty',
      'sec-fetch-mode':
      'cors',
      'sec-fetch-site':
      'same-origin',
      'sec-gpc':
      '1',
      'user-agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  }

  params = {'shorturl': shorturl}

  if password:
    params['pwd'] = password

  try:
    # Get video information
    response_info = requests.get(url + "/api/get-info",
                                 headers=headers,
                                 params=params)
    response_info.raise_for_status()
    video_info = response_info.json()

    # Prepare data for downloading
    data = {
        "shareid": video_info.get("shareid"),
        "uk": video_info.get("uk"),
        "sign": video_info.get("sign"),
        "timestamp": video_info.get("timestamp"),
        "fs_id": video_info.get("list")[0].get("fs_id")
    }

    # Download video
    response_download = requests.post(url + "/api/get-download",
                                      headers=headers,
                                      json=data)
    response_download.raise_for_status()
    download_url = response_download.json().get('downloadLink')

    return s.tinyurl.short(download_url)
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return e
  except Exception as e:
    return e
