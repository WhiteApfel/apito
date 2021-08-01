import urllib.parse
from typing import Union

from httpx import AsyncClient, Client
from httpx_socks import AsyncProxyTransport

from apito.models.phone import PhoneInfo
from apito.models.search import SearchAnswer


class Aiopito:
    def __init__(self, cookies: str = None):
        self.__client = None
        self.__cookies = cookies
        self.__key = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"

    @property
    def client(self):
        if not self.__client:
            self.__client = AsyncClient()
        return self.__client

    async def search_generator(self,
                               query: str,
                               cookies: str = None,
                               location_id: Union[str, int] = 640860,
                               search_radius: int = 0,
                               start_page: int = 1,
                               stack: bool = False,
                               stop_me_noooow: bool = True,
                               proxy: str = None):

        ya_zhe_kto_to_drugoy_drugogo_tsveta_dazhe = True

        while ya_zhe_kto_to_drugoy_drugogo_tsveta_dazhe:
            res = await self.search(query, cookies, location_id, search_radius, start_page)

            if res.status == 'ok' and len(res.result.items):
                start_page += 1

                if stop_me_noooow:
                    to_yield = []

                    for item in res.result.items:
                        if item.type != 'groupTitle':
                            if not stack:
                                yield item
                            else:
                                to_yield.append(item)
                        else:
                            ya_zhe_kto_to_drugoy_drugogo_tsveta_dazhe = False
                            break

                    if not stack:
                        yield to_yield

                else:
                    to_yield = [i for i in res.result.items if i.type != 'groupTitle']
                    yield to_yield

            else:
                ya_zhe_kto_to_drugoy_drugogo_tsveta_dazhe = False

    async def search(self, query: str, cookies: str = None, location_id: Union[str, int] = 640860, search_radius: int = 0, page: int = 1, proxy: str = None):
        url = "https://m.avito.ru/api/11/items"

        params = {
            "key": self.__key,
            "query": query,
            "locationId": location_id,
            "searchRadius": search_radius,
            "page": page,
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
        if cookies:
            headers['Cookie'] = cookies

        if proxy:
            transport = AsyncProxyTransport.from_url(proxy)
            with AsyncClient(transport=transport) as client:
                response = await client.get(url, headers=headers, params=params)
        else:
            response = await self.client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            response_model = SearchAnswer(**data)
            return response_model
        else:
            raise ValueError(f"{response.status_code} - {response.text}")

    def item_contact_phone(self, item_id: int, cookies: str = None, proxy: str = None):
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

            if proxy:
                transport = AsyncProxyTransport.from_url(proxy)
                with AsyncClient(transport=transport) as client:
                    response = await client.get(url, headers=headers)
            else:
                response = await self.client.get(url, headers=headers)

            if response.status_code == 200:
                response_json = response.json()
                if response_json['status'] == 'ok':
                    phone = urllib.parse.unquote(response_json['result']['action']['uri'].split('=')[-1])
                    return PhoneInfo(success=True, phone=phone, message=None)
                elif response_json['status'] == 'bad-request':
                    message = response_json['result']['message']
                else:
                    message = 'Unsuccessful'
            else:
                message = f"{response.status_code} - {response.text}"
            return PhoneInfo(success=False, phone=None, message=message)
        raise ValueError('No cookies were specified when the class was initialized or when the method was called.')

