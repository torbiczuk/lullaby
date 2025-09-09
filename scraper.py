import asyncio
import aiohttp
import re
import json

class SeatScraper:
    def __init__(self):
        self.urls = {
            "2025-09-28": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808326#overall",
            "2025-10-04": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808301#overall",
            "2025-10-05": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808304#overall",
            "2025-10-11": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808305#overall",
        }

    async def fetch_html(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def extract_seats(self, html):
        match = re.search(r"var\s+seats\s*=\s*(\[.*?\]);", html, re.S)
        if not match:
            return []
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return []

    async def get_all_seats_data(self):
        results = []
        
        async with aiohttp.ClientSession() as session:
            htmls = await asyncio.gather(*(self.fetch_html(session, url) for url in self.urls.values()))

        free_total = 0
        taken_total = 0
        all_total = 0

        for (date, url), html in zip(self.urls.items(), htmls):
            seats = self.extract_seats(html)
            seats = [s for s in seats if s.get("type") == "seat"]

            free = sum(1 for s in seats if not s.get("isUnavailable", True))
            taken = sum(1 for s in seats if s.get("isUnavailable", True))
            total = len(seats)
            free_percent = (free / total * 100) if total > 0 else 0

            free_total += free
            taken_total += taken
            all_total += total

            results.append({
                'date': date,
                'free': free,
                'taken': taken,
                'total': total,
                'free_percent': round(free_percent, 1),
                'url': url
            })

        total_percent = (free_total / all_total * 100) if all_total > 0 else 0
        
        return {
            'events': results,
            'summary': {
                'free_total': free_total,
                'taken_total': taken_total,
                'all_total': all_total,
                'total_percent': round(total_percent, 1)
            }
        }