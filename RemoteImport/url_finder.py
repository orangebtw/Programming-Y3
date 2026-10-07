from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
from urlloader import URLLoader
from urllib.parse import urlparse

class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available
        
    def find_spec(self, name, target=None):
        for avail in self.available:
            is_package = avail.endswith('/')
            path_segments = name.replace('.', '/')
            
            if path_segments == avail.rstrip('/'):
                parsed = urlparse(self.url)
                host = f"{parsed.scheme}://{parsed.netloc}"
                
                if is_package:
                    origin = "{}/{}/__init__.py".format(host, path_segments)
                else:
                    origin = "{}/{}.py".format(host, path_segments)
                
                spec = spec_from_loader(name, URLLoader(), origin=origin, is_package=is_package)
                if is_package:
                    spec.submodule_search_locations = [f"{host}/{path_segments}/"]
                return spec
        
        return None