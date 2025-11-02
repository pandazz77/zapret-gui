import requests
import base64


def get_files_list(owner:str, repo:str, path:str="", branch:str='main') -> list[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")

    return [item["path"] for item in response.json()]

def get_file_content_api(owner:str, repo:str, file_path:str, branch:str='main') -> bytes:
    """
        Get file content via github api.
        WARNING: RATELIMIT
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
    
    content = response.json()
    file_content = base64.b64decode(content['content'])
    return file_content

def get_file_content_raw(owner:str, repo:str, file_path:str, branch:str='main') -> bytes:
    """
        Get file content via raw.githubusercontent.
    """
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error: {response.status_code}")
    

if __name__ == "__main__":
    USERNAME = "Flowseal"
    REPONAME = "zapret-discord-youtube"
    raw = get_file_content_raw(USERNAME,REPONAME,"README.md")
    print(raw.decode())