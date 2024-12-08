import json
import requests
import multiprocessing
import time


def execute_process(url: str, queue: multiprocessing.Queue, index: int) -> None:
    data_js = requests.get(url).json()
    data_str = json.dumps(data_js)
    print(f"Process {index} Downloaded {len(data_str)} chars from {url}")
    
    queue.put(len(data_str))

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

    queue = multiprocessing.Queue()
    processes = []
    for index, url in enumerate(urls):
        process = multiprocessing.Process(target=execute_process, args=(url, queue, index, ))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    for process in processes:
        TOTAL_CHARS += queue.get()

    print(f"Total number of chars downloaded is {TOTAL_CHARS}")


TOTAL_CHARS = 0


if __name__ == "__main__":
    main()
