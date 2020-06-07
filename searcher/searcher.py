# -*- coding: utf-8 -*-
import time

import ujson
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options


yandex = {
    'url': 'http://yandex.ru/search/?text=',
    'xpath_results': '//a[contains(@class, "link_cropped_no")]'
}
google = {
    'url': 'http://google.com/search?q=',
    'xpath_results': '//a[h3]'
}
selenium_url = 'http://localhost:4444/wd/hub'


class Link:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f'{self.title}\n{self.url}'


def output_to_console(links):
    for link in links:
        print(link)


def output_to_json(links):
    new_links = []
    for link in links:
        new_link = link.__dict__
        new_links.append(new_link)
    with open('links.json', 'w', encoding='utf-8') as w:
        w.write(ujson.dumps(new_links, indent=4, ensure_ascii=False))


def output_to_csv(links):
    rows = []
    for link in links:
        row = f'{link.title};{link.url}\n'
        rows.append(row)
    with open('links.csv', 'w', encoding='utf-8') as w:
        w.writelines(rows)


def get_title_from_inner_text(text):
    return text.strip().split('\n')[0]


def search(engine: dict, req, lim):
    driver.get(f'{engine.get("url")}{req}')
    time.sleep(1)
    links = driver.find_elements_by_xpath(engine.get('xpath_results'))
    return parse_links(links, lim)


def search_on_page(url, lim):
    driver.get(url)
    time.sleep(1)
    links = driver.find_elements_by_tag_name('a')
    return parse_links(links, lim)


def parse_links(links, lim):
    results = []
    count = 0
    for link in links:
        if count >= lim:
            break
        title = get_title_from_inner_text(link.get_attribute('innerText'))
        url = link.get_attribute('href')
        if not url:
            continue
        count += 1
        results.append(Link(title, url))
    return results


def check_empty_field(string):
    if not string.strip():
        raise ValueError('Поле не может быть пустым')
    return string


def read_request(string):
    try:
        req = check_empty_field(input(f'{string}\n').lower())
        return req
    except ValueError as e:
        print(e)
        read_request(string)


def read_limit(string):
    try:
        lim = int(input(f'{string}\n'))
        if not lim or lim < 1:
            raise ValueError('Неправильное значение. Введите число')
        return int(lim)
    except ValueError as e:
        print(e)
        read_limit(string)


def choose_between_two(string, first, second):
    try:
        answer = check_empty_field(input(f'{string} ({first}/{second})\n').lower())
        if answer == first or answer == second:
            return answer
        raise ValueError(f'Выберите {first} или {second}')
    except ValueError as e:
        print(e)
        choose_between_two(string, first, second)


def choose_from_three(string, first, second, third):
    try:
        answer = check_empty_field(input(f'{string} ({first}/{second}/{third})\n').lower())
        if answer == first or answer == second or answer == third:
            return answer
        raise ValueError(f'Выберите {first}, {second} или {third}')
    except ValueError as e:
        print(e)
        choose_from_three(string, first, second, third)


def get_links(engine, req, lim):
    if engine == 'yandex':
        return search(yandex, req, lim)
    return search(google, req, lim)


def output_results(out, results):
    if out == 'console':
        output_to_console(results)
    elif out == 'json':
        output_to_json(results)
    elif out == 'csv':
        output_to_csv(results)


def start_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    return Remote(command_executor=selenium_url,
                  desired_capabilities=chrome_options.to_capabilities())


if __name__ == '__main__':
    request = read_request('Что ищем?')
    search_engine = choose_between_two('Где ищем?', 'yandex', 'google')
    limit = read_limit('Сколько нужно результатов?')
    recursion = choose_between_two('Забираем ссылки из найденного?', 'y', 'n')
    output = choose_from_three('В каком формате сохраняем?', 'json', 'csv', 'console')

    driver = start_driver()

    search_results = get_links(search_engine, request, limit)

    if recursion == 'y':
        temp_results = []
        for result in search_results:
            temp_results.extend(search_on_page(result.url, limit))
        search_results.extend(temp_results)

    output_results(output, search_results)
    driver.close()
