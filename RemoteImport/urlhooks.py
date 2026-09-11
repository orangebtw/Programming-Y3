from url_finder import URLFinder
import re
import sys
import requests
from urllib.parse import urljoin, urlparse

def find_all_files(content: str, base_url: str, paths: list, parent: str | None):
    filenames = re.findall(r"<li><a\s+href=\".*\">([a-zA-Z_][a-zA-Z0-9_]*(?:.py|/))<\/a><\/li>", content)
    
    has_init_py = any(map(lambda x: x.endswith('__init__.py'), filenames))
    
    if not has_init_py and parent is not None:
        return
    
    for name in filenames:
        url = urljoin(base_url, name)
        if name.endswith('__init__.py'):
            continue
        
        path = name if parent is None else parent + name
        paths.append(path.rstrip('.py'))
        
        if name.endswith('/'):
            response = requests.get(url)
            find_all_files(response.text, url, paths, name)
        

def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    
    try:
        response = requests.get(some_str)
    except requests.ConnectionError:
        return URLFinder(some_str, {})
    
    paths = []
    find_all_files(response.text, some_str, paths, None)
    
    return URLFinder(some_str, paths)


sys.path_hooks.append(url_hook)
print(sys.path_hooks)