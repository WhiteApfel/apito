import urllib.parse
from typing import Union

from httpx import Client

from apito.models.phone import PhoneInfo
from apito.models.search import SearchAnswer


class Apito:
    def __init__(self, cookies: str = None):
        self.__client = None
        self.__cookies = cookies
        self.__key = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"

    @property
    def client(self):
        if not self.__client:
            self.__client = Client()
        return self.__client

    def search(self, query: str, location_id: Union[str, int] = 640860, search_radius: int = 0):
        import requests

        url = "https://m.avito.ru/api/11/items"

        params = {
            "key": self.__key,
            "query": query,
            "locationId": location_id,
            "searchRadius": search_radius,
            "page": 1,
            "display": "list",
            "limit": 30
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) Chrome/90.0.4430.91',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json;charset=utf-8',
            'Connection': 'keep-alive',
            'Referer': 'https://m.avito.ru/nizhniy_novgorod/?q=Don%27t%2Bbe%2Bafraid%2Bgirl&radius=0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }

        response = self.client.get(url, headers=headers, params=params)

        response_model = SearchAnswer(**response.json())

        return response_model

    def item_contact_phone(self, item_id: int, cookies: str = None):
        if self.__cookies or cookies:
            url = f"https://m.avito.ru/api/1/items/{item_id}/phone?key={self.__key}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) Chrome/90.0.4430.91',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json;charset=utf-8',
                'Connection': 'keep-alive',
                'Referer': 'https://m.avito.ru/nizhniy_novgorod/odezhda_obuv_aksessuary/nosochki_detskie_zhenskie_i_'
                           'muzhskie_1937484816',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Cookie': self.__cookies or cookies
            }

            response = self.client.get(url, headers=headers)

            if response.status_code == 200:
                response_json = response.json()
                if response_json['status'] == 'ok':
                    phone = urllib.parse.unquote(response['result']['action']['uri'].split('=')[-1])
                    return PhoneInfo(success=True, phone=phone, message=None)
                elif response_json['status'] == 'bad-request':
                    message = response_json['result']['message']
                else:
                    message = 'Unsuccessful'
                return PhoneInfo(success=False, phone=None, message=message)
        raise ValueError('No cookies were specified when the class was initialized or when the method was called.')

