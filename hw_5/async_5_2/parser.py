import asyncio
import json
from datetime import datetime
import random
from typing import List

import aiofiles
from bs4 import BeautifulSoup
from aiohttp import ClientSession, TCPConnector
from fake_useragent import UserAgent


class YandexRealtyParser:
    def __init__(self):
        self.base_url = "https://realty.yandex.ru"
        self.search_url = f"{self.base_url}/sankt-peterburg/snyat/kvartira/"
        self.headers = {
            'Accept': '*/*',
            'User-Agent': UserAgent().random,
            "Accept-Language": "ru-RU,ru;q=0.9"
        }
        self.offers = []
        self.seen_offers = set()

    async def fetch_page(self, session, url: str) -> str:
        """Загружает HTML страницы"""
        try:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                print(f'Download url: {url}')
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    async def get_offer_links(self, session, page_num: int) -> List[str]:
        """Получает список ссылок на объявления с одной страницы поиска"""
        url = f"{self.search_url}?sort=DATE_DESC&page={page_num}"
        html = await self.fetch_page(session, url)
        soup = BeautifulSoup(html, 'html.parser')

        links = []
        for offer_link in soup.select("a.OffersSerpItem__titleLink"):
            full_url = self.base_url + offer_link['href']
            if full_url not in self.seen_offers:
                links.append(full_url)
                self.seen_offers.add(full_url)

        links = list(set(links))
        return links

    async def parse_offer_page(self, session, offer_url: str):
        """Парсит страницу объявления"""
        html = await self.fetch_page(session, offer_url)
        soup = BeautifulSoup(html, 'html.parser')

        title = self._clean_text(soup.select_one('h1.OfferCardSummaryInfo__description--3-iC7'))
        price = self._clean_text(soup.select_one('span.OfferCardSummaryInfo__price--2FD3C')).split('₽')[0].strip()
        address = self._get_address(soup)
        floor = self._parse_floor(soup)

        area = self._get_feature(soup, 'общая')
        area = area.split()[0] if area else 'Не указана'
        year = self._get_feature(soup, 'год постройки')
        year = year.replace('год', '').strip() if year else 'Не указан'

        return {
            'id': offer_url.split('/')[-2],
            'title': title,
            'price, rub': price,
            'address': address,
            'floor': floor,
            'area, м²': area,
            'year': year,
            'url': offer_url
        }

    async def save_to_json(self, file_path: str = "../artifacts/offers_5_2.json"):
        """сохраняет данные в файл json"""
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(self.offers, ensure_ascii=False, indent=2))

    async def monitor_new_offers(self, page_num: int = 1, interval: int = 3600):
        """Проверяет на наличие новых объявлений"""
        connector = TCPConnector(limit=10, force_close=False, enable_cleanup_closed=True)
        async with ClientSession(connector=connector) as session:
            while True:
                print(f"Checking for new offers at {datetime.now()}")

                all_links = []
                for page in range(1, page_num + 1):
                    await asyncio.sleep(random.uniform(1, 3))
                    links = await self.get_offer_links(session, page)
                    all_links.extend(links)

                semaphore = asyncio.Semaphore(3)

                async def limited_parse(url):
                    async with semaphore:
                        await asyncio.sleep(random.uniform(0.5, 2))
                        return await self.parse_offer_page(session, url)

                tasks = [limited_parse(url) for url in all_links]
                new_offers = await asyncio.gather(*tasks)

                for offer in new_offers:
                    if offer and offer['url'] not in [o['url'] for o in self.offers]:
                        self.offers.append(offer)
                        print(f"New offer found: {offer['title']} | {offer['price, rub']}")

                await self.save_to_json()
                print(f"Waiting {interval // 60} minutes before next check...")
                await asyncio.sleep(interval)

    @staticmethod
    def _clean_text(elem) -> str:
        """Извлекает и очищает текст из элемента"""
        return elem.get_text(' ', strip=True) if elem else ''

    def _get_address(self, soup) -> str:
        """Извлекает адрес"""
        h3 = soup.find('h3', class_='OfferCardExtendedLocationInfo__title--3ICax')
        if not h3:
            return "Не указан"

        section = h3.find_next_sibling(class_='GeoLinks__geoLinks--MN9-6')
        if not section:
            return "Не указан"

        container = section.find('div', class_='AddressWithGeoLinks__addressContainer--4jzfZ')
        if not container:
            return "Не указан"

        address_parts = []
        for link in container.find_all('a', class_='Link'):
            text = self._clean_text(link)
            if text:
                address_parts.append(text)

        for element in container.children:
            if isinstance(element, str):
                text = element.strip(' ,"\n\t')
                if text and text not in ('<!-- -->', ','):
                    house_num = ''.join(c for c in text if c.isalnum())
                    if house_num:
                        address_parts.append(text)

        full_address = ', '.join(filter(None, address_parts))
        return full_address.replace('  ', ' ').strip()

    def _get_feature(self, soup, feature_name: str) -> str:
        """Извлекает значение характеристики по названию"""
        containers = soup.find_all(class_='OfferCardHighlight__container--2gZn2')
        for container in containers:
            label = container.find(class_='OfferCardHighlight__label--2uMCy')
            if label and feature_name in label.get_text(strip=True).lower():
                value = container.find(class_='OfferCardHighlight__value--HMVgP')
                if value:
                    feature = self._clean_text(value)
                    return feature
        return ''

    @staticmethod
    def _parse_floor(soup):
        """Извлекает номер этажа"""
        features = soup.select('.OfferCardHighlight__value--HMVgP')

        for feature in features:
            text = feature.get_text(strip=True)
            if 'этаж' in text.lower():
                floor = text.split()[0]

                label = feature.find_next_sibling(class_='OfferCardHighlight__label--2uMCy')
                total_floors = label.get_text(strip=True).split()[-1] if label else '?'

                return f"{floor}/{total_floors}"

        return "Не указан"


async def main():
    parser = YandexRealtyParser()
    await parser.monitor_new_offers(interval=1800)


if __name__ == "__main__":
    asyncio.run(main())
