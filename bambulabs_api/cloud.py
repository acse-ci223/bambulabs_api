from base64 import b64decode
import json
import requests

class Cloud:
    def __init__(self, email, region, username=None, token=None):
        self._email = email
        self._region = region
        self._username = username
        self._token = token
        tld = "cn" if self._region == "China" else "com"
        self._api_url = f'https://api.bambulab.{tld}/v1'

    def login(self, password):
        credentials = {'account': self._email, 'password': password}
        res = requests.post(f'{self._api_url}/user-service/user/login', json=credentials, timeout=10)
        if not res.ok:
            raise ValueError(res.status_code)
        self._token = res.json()['accessToken']

        # extract username from tokens 2nd part
        payload = self._token.split('.')[1]
        # fix base64 padding
        payload += '=' * ((4 - len(payload) % 4) % 4)
        # decode string, convert to json and return username
        self._username = json.loads(b64decode(payload))['username']

    def get_token(self) -> str:
        return self._token

    def get_username(self) -> str:
        return self._username

    def get_devices(self) -> dict:
        headers = {'Authorization': 'Bearer ' + self._token}
        res = requests.get(f'{self._api_url}/iot-service/api/user/bind', headers=headers, timeout=10)
        if not res.ok:
            raise ValueError(res.status_code)
        return res.json()['devices']
