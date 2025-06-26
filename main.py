import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin
import time

# Лимит запросов в секунду
RATE_LIMIT_PER_SECOND = 10

def fetch_page(url):
    """Загрузка страницы"""
    try:
        print(f"[DEBUG]: Загрузка страницы {url}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f'Ошибка HTTP {response.status_code}')
        return response.text
    except Exception as e:
        print(f'[ERROR]: Ошибка загрузки страницы {url}: {e}')
        return None

def extract_links(soup, base_url):
    """Извлечение только внутренних ссылок из центрального содержимого статьи"""
    content_div = soup.find('div', id='mw-content-text')
    if not content_div:
        return []

    links = set()
    for link in content_div.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and not ':' in href.split('/')[-1]:
            full_url = urljoin(base_url, href)
            links.add(full_url)

    print(f"[DEBUG]: Количество извлечённых ссылок: {len(links)}")
    return list(links)

def advanced_bfs(start_url, target_url, rate_limit_per_second):
    """Поиск кратчайшего пути между двумя страницами методом BFS"""
    MAX_DEPTH = 5
    queue = deque([[start_url]])
    visited_pages = set()
    iteration = 0

    while queue:
        iteration += 1
        path = queue.popleft()
        current_url = path[-1]
        depth = len(path) - 1

        if depth >= MAX_DEPTH:
            continue

        if current_url in visited_pages:
            continue
        visited_pages.add(current_url)

        print(f"[DEBUG]: Итерация #{iteration}, Глубина {depth}, Исследуется {current_url}")
        html = fetch_page(current_url)
        if not html:
            continue

        soup = BeautifulSoup(html, 'lxml')
        links = extract_links(soup, start_url)

        time.sleep(1 / rate_limit_per_second)

        for next_url in links:
            if next_url in visited_pages:
                continue

            new_path = list(path)
            new_path.append(next_url)

            if next_url == target_url:
                return new_path

            queue.append(new_path)

    return []  # Если путь не найден

if __name__ == "__main__":
    print("=== Wikipedia Path Finder ===")
    start_url = input("Введите начальную ссылку: ").strip()
    end_url = input("Введите конечную ссылку: ").strip()
    rate_limit_input = input("Укажите лимит запросов в секунду [по умолчанию 10]: ").strip()
    rate_limit = int(rate_limit_input) if rate_limit_input.isdigit() else RATE_LIMIT_PER_SECOND

    print("[INFO]: Поиск пути от A к B...")
    path1 = advanced_bfs(start_url, end_url, rate_limit)
    if path1:
        print("[RESULT]: Путь A -> B:")
        for step in path1:
            print(step)
    else:
        print("[WARNING]: Путь от A к B не найден.")

    print("[INFO]: Поиск пути от B к A...")
    path2 = advanced_bfs(end_url, start_url, rate_limit)
    if path2:
        print("[RESULT]: Путь B -> A:")
        for step in path2:
            print(step)
    else:
        print("[WARNING]: Путь от B к A не найден.")
