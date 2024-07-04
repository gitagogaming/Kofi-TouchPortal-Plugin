#update check
import os
import base64
import requests
from tempfile import gettempdir

from TPPEntry import GITHUB_USER_NAME, GITHUB_PLUGIN_NAME    


def plugin_update_check(plugin_version:str):
    """ Checks Github for the latest version of the plugin
    - Returns patchnotes on notification if there is a new version 
    """
    
    try:
        github_version, download_url, html_url = _get_release_info(GITHUB_USER_NAME, GITHUB_PLUGIN_NAME)
        github_version =  github_version.replace('v','').replace(".","")
      
        if github_version > plugin_version:
            patch_notes = _fetch_patch_notes(GITHUB_USER_NAME, GITHUB_PLUGIN_NAME)
            return {"version":github_version, "patchnotes":patch_notes, "downloadURL": download_url, "htmlURL": html_url}
        else:
            return False, False
        
    except Exception as e:
        print("Something went wrong checking update", e)
 
 
 
def _fetch_patch_notes(user_name: str, plugin_name: str) -> str:
    """Fetches and decodes patch notes from GitHub."""
    patch_notes_url = f"https://api.github.com/repos/{user_name}/{plugin_name}/contents/recent_patchnotes.txt"
    response = requests.get(patch_notes_url)
    if response.status_code == 404:
        print("No Patch Notes Found")
        return ""
    try:
        content = response.json()['content']
        decoded_bytes = base64.b64decode(content)
        return decoded_bytes.decode('ascii')
    except Exception as e:
        print(f"Error fetching patch notes: {e}")
        return None
        

def _get_release_info(owner, repo):
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


