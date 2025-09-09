import asyncio
import aiohttp
import re
import json
from tabulate import tabulate

URLS = {
    "2025-09-28": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808326#overall",
    "2025-10-04": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808301#overall",
    "2025-10-05": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808304#overall",
    "2025-10-11": "https://www.bilety24.pl/kup-bilet-na-631-lullaby-136682?id=808305#overall",
}


async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()


def extract_seats(html):
    """Wyciąga listę seats z HTML-a"""
    match = re.search(r"var\s+seats\s*=\s*(\[.*?\]);", html, re.S)
    if not match:
        return []
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return []


async def main():
    results = []

    async with aiohttp.ClientSession() as session:
        htmls = await asyncio.gather(*(fetch_html(session, url) for url in URLS.values()))

    free_total = 0
    taken_total = 0
    all_total = 0

    for (date, url), html in zip(URLS.items(), htmls):
        seats = extract_seats(html)
        seats = [s for s in seats if s.get("type") == "seat"]

        free = sum(1 for s in seats if not s.get("isUnavailable", True))
        taken = sum(1 for s in seats if s.get("isUnavailable", True))
        total = len(seats)
        free_percent = (free / total * 100) if total > 0 else 0

        free_total += free
        taken_total += taken
        all_total += total

        results.append([date, free, taken, total, f"{free_percent:.1f}%", url])

    # Dodajemy wiersz sumaryczny
    total_percent = (free_total / all_total * 100) if all_total > 0 else 0
    results.append(["SUMA", free_total, taken_total, all_total, f"{total_percent:.1f}%", ""])

    print(tabulate(results, headers=["Data", "Wolne", "Zajęte", "Łącznie", "% Wolnych", "URL"], tablefmt="grid"))


if __name__ == "__main__":
    asyncio.run(main())
