from setuptools import setup
from io import open


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


def requirements():
    with open('requirements.txt', 'r') as req:
        return [r for r in req.read().split("\n") if r]


setup(
    name='apito',
    version='0.4.3',
    packages=['apito', 'apito.models'],
    url='https://github.com/WhiteApfel/apito',
    license='MPL 2.0',
    author='WhiteApfel',
    author_email='white@pfel.ru',
    description='Avito API interaction tool ',
    install_requires=requirements(),
    project_urls={
        "Donate": "https://pfel.cc/donate",
        "Source": "https://github.com/WhiteApfel/apito",
        "Telegram": "https://t.me/apfel"
    },
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    keywords='Avito API Wrapper Parser Авито АПИ парсер'
)
