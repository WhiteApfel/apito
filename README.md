# Apito

This tool accesses the API directly, rather than loading the site and iterating over the tags.

## Installation

```shell
python -m pip install -U apito

# OR

git clone https://github.com/WhiteApfel/apito.git
cd apito
python setup.py install
```

## How to use

```python
import asyncio
from apito import Apito, Aiopito

# sync

a = Apito()

response = a.search('Моё сердечко', proxy="socks5://ya_slovno:vys0hsHaYa@luzha:2005")

if response.status == 'ok':
    print('Total found: ', response.result.total_count())
    for item in response.result.items:
        print(f'{item.value.title} @ {item.value.location or item.value.address}')
        print(f'Price: {item.value.price}')

results = a.search_generator("Упущенные возможности")

for item in results:
    print(f"{item.value.title} #{item.value.id}")

# async

a = Aiopito()


async def main():
    print((await a.search("Носочки для новорождённых")).result.count)

    async for x in a.search_generator("Носочки для новорождённых"):
        print(x)


asyncio.run(main())
```