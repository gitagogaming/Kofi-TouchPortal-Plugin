#update check
import os
import base64
import requests
from tempfile import gettempdir

from TPPEntry import GITHUB_USER_NAME, GITHUB_PLUGIN_NAME    


def get_release_info(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    if (response := requests.get(url)) and response.ok:
        if (releases := response.json()):
            for release in releases:
                if not release.get('prerelease'):
                    assets = release.get('assets', [])
                    if assets:
                        download_url = assets[0].get('browser_download_url', "")
                        release_version = release.get('tag_name', "")
                        html_url = release.get('html_url', "")
                        return release_version, download_url, html_url
            raise ValueError(f'No suitable non-prerelease found in repository: {url}')
        else:
            raise ValueError(f'Failed to decode JSON response from: {url}')
    else:
        raise ValueError(f'Invalid repository URL or response: {url}')


def plugin_update_check(plugin_version:str):
    """ Checks Github for the latest version of the plugin
    - Returns patchnotes on notification if there is a new version 
    """
    
    try:
        github_version, downloadURL, htmlURL = get_release_info(GITHUB_USER_NAME, GITHUB_PLUGIN_NAME)
        github_version =  github_version.replace('v','').replace(".","")
      
        if github_version.replace('v','').replace(".","") > plugin_version:
            ### Pulling Patch Notes for Notification

            try:
                r = requests.get(f"https://api.github.com/repos/{GITHUB_USER_NAME}/{GITHUB_PLUGIN_NAME}/contents/recent_patchnotes.txt") 
                if r.status_code == 404:
                    print("No Patch Notes Found")
                    message = ""
                else:
                    base64_bytes = r.json()['content'].encode('ascii')
                    message_bytes = base64.b64decode(base64_bytes)
                    message = message_bytes.decode('ascii')
            except Exception as e:
                message = None
                print("Error Plugin Update Check: ", e)
            return {"version":github_version, "patchnotes":message, "downloadURL": downloadURL, "htmlURL": htmlURL}
        else:
            return False, False
        
    except Exception as e:
        print("Something went wrong checking update", e)
        
        

def download_update(download_url):
    # Extract the file name from the URL
    file_name = download_url.split('/')[-1]
    # Construct the full path in the temp directory
    temp_file_path = os.path.join(gettempdir(), file_name)
    
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(temp_file_path, 'wb') as file:
            file.write(response.content)
            return temp_file_path
    return None