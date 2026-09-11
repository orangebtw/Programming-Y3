from url_finder import URLFinder
import re
import sys
import requests

def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    
    try:
        response = requests.get(some_str)
    except requests.ConnectionError:
        return URLFinder(some_str, {})
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", response.text)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)
print(sys.path_hooks)