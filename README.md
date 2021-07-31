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
from apito import Apito

a = Apito()

response = a.search('Моё сердечко')

if response.status == 'ok':
    print('Total found: ', response.result.total_count())
    for item in response.result.items:
        print(f'{item.value.title} @ {item.value.location or item.value.address}')
        print(f'Price: {item.value.price}')
```