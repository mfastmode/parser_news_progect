import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://kostroma.aif.ru/news/region'


# Функция для получения HTML-страницы
def fetch_page(url, headers, proxies):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        print(f"Ошибка: {response.status_code}")
        return None

# Функция для извлечения ссылок из списка новостей
def extract_links(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('div', class_='list_item')
    links = [item.find('a').get('href') for item in news if item.find('a')]
    return links

# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', itemprop='headline').get_text(strip=True)
    text = soup.find('div', class_='article_text').get_text(strip=True)
    time = soup.find('b', class_='first_float').get_text(strip=True)
    return f"\n\nВремя: {time}\nЗаголовок: {title}\nОписание:\n{text}"

# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
if main_page_html:
    # Извлекаем ссылки на новости
    links_news_description = extract_links(main_page_html)
    
    with open('pars_result00.txt', 'w', encoding='utf-8') as f:
        # Обрабатываем каждую новость
        for link in links_news_description:
            article_html = fetch_page(link, headers, proxy_auth)
            if article_html:
                # Извлекаем данные и записываем в файл
                article_data = extract_article_data(article_html)
                
                f.write(article_data)
                f.write("\n" + "-" * 100 + "\n")  # Разделитель между постами