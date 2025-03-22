import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://smi44.ru/news/'


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
    
    divs = soup.find_all('div', {'class': 'news_item medium-4 large-3 columns'})
    urls_news = []
    for div in divs:
        url_pars = div.find('div', {'class': 'img_preview_wrapper'})
        url = url_pars.find('a').get('href')
        result_url = f'https://smi44.ru{url}'
        urls_news.append(result_url)
  
    return urls_news

# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Заголовок
    title = soup.find('div', {'class': 'news-detail'}).find('h1').get_text()
    # Время
    time = soup.find('span', {'class': 'news-date-time'}).get_text()
    # Описание
    content = soup.find('div', {'id': 'detail_news_text'})
    text = content.get_text(strip=True)
    
    return f"\n\nВремя: {time}\nЗаголовок: {title}\nОписание:\n{text}"

# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result06.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами