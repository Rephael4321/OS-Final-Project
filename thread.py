import json
import requests
import threading


TOTAL_CHARS = 0


def execute_thread(url: str, mutex: threading.Lock, index: int) -> None:
    global TOTAL_CHARS

    data_js = requests.get(url).json()
    data_str = json.dumps(data_js)
    print(f"Thread {index} Downloaded {len(data_str)} chars from {url}")

    with mutex:
        TOTAL_CHARS += len(data_str)


def main() -> None:
    global TOTAL_CHARS
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]

    mutex = threading.Lock()
    threads = []
    for index, url in enumerate(urls):
        thread = threading.Thread(target=execute_thread, args=(url, mutex, index, ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Total number of chars downloaded is {TOTAL_CHARS}")


if __name__ == "__main__":
    main()
