import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse, urljoin
import time

# Лимит запросов в секунду
RATE_LIMIT_PER_SECOND = 10

def fetch_page(url):
    """Загрузка страницы"""
    try:
        print(f"[DEBUG]: Загрузка страницы {url}")
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f'Ошибка HTTP {response.status_code}')
        return response.text
    except Exception as e:
        print(f'[ERROR]: Ошибка загрузки страницы {url}: {e}')
        return None

def extract_links(soup, base_url):
    """
    Извлечение внутренних ссылок на вики-статьи
    """
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_link = urljoin(base_url, href)
        if '/wiki/' in href and ':' not in href.split('/')[-1]:
            links.add(full_link)

    print(f"[DEBUG]: Количество извлечённых ссылок: {len(links)}")
    return list(links)

def advanced_bfs(start_url, target_url, rate_limit_per_second):
    """
    Поиск кратчайшего пути между двумя страницами методом BFS с продвинутым контролем очереди
    """
    MAX_QUEUE_SIZE = 1000                  # Максимальный размер очереди
    MAX_DEPTH = 5                           # Максимально допустимый уровень глубины
    queue = deque([[start_url]])            # Очередь поиска начинается с начальной страницы
    visited_pages = set()                    # Посещённые страницы
    iteration_count = 0                      # Текущий номер итерации

    while queue:
        iteration_count += 1
        path = queue.popleft()
        current_url = path[-1]
        depth = len(path) - 1                # Первый узел — нулевого уровня

        # Если достигнут максимальный уровень глубины, прекращаем
        if depth >= MAX_DEPTH:
            continue

        # Отчёты о ходе поиска
        print(f"[DEBUG]: Итерация #{iteration_count}, Глубина {depth}, Очередь имеет длину {len(queue)}, Исследование страницы {current_url}")

        # Если страница уже была посещена, пропускаем её
        if current_url in visited_pages:
            continue

        # Фиксируем факт посещения страницы
        visited_pages.add(current_url)

        # Загружаем страницу и проверяем результат
        page_html = fetch_page(current_url)
        if page_html is None:
            continue

        # Анализируем страницу и извлекаем ссылки
        soup = BeautifulSoup(page_html, 'lxml')
        links = extract_links(soup, start_url)

        # Пауза между запросами
        time.sleep(1 / rate_limit_per_second)

        for next_url in links:
            if next_url in visited_pages:
                continue

            new_path = list(path)
            new_path.append(next_url)

            if next_url == target_url:
                return new_path

            queue.append(new_path)

            # Если очередь становится слишком большой, отрезаем её до приемлемых размеров
            if len(queue) > MAX_QUEUE_SIZE:
                print(f"[WARNING]: Очередь превысила допустимый размер ({MAX_QUEUE_SIZE}), проводим сокращение.")
                queue = deque(list(queue)[len(queue)-MAX_QUEUE_SIZE:])

    return []  # Возвращаем пустой список, если путь не найден

if __name__ == "__main__":
    start_url = input("Введите начальную ссылку: ").strip()
    end_url = input("Введите конечную ссылку: ").strip()
    rate_limit_input = input("Укажите лимит запросов в секунду: ").strip()

    try:
        rate_limit = int(rate_limit_input)
    except ValueError:
        print("Некорректный ввод для лимита запросов. Используйте целое число.")
        exit(1)

    # Основной поиск путей
    print("[INFO]: Начинаем поиск пути...")
    result_forward = advanced_bfs(start_url, end_url, rate_limit)
    result_backward = advanced_bfs(end_url, start_url, rate_limit)

    if result_forward:
        print(f"{start_url} -> {' -> '.join(result_forward)}")
    else:
        print(f"Путь от {start_url} до {end_url} не найден.")

    if result_backward:
        print(f"{end_url} -> {' -> '.join(result_backward)}")
    else:
        print(f"Путь от {end_url} до {start_url} не найден.")
