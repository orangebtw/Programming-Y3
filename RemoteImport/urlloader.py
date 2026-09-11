import requests

class URLLoader:
    def create_module(self, target):
        return None
    
    def exec_module(self, module):
        response = requests.get(module.__spec__.origin)
        code = compile(response.text, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)