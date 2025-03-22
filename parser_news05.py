import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://kostroma.today/'


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
    
    divs = soup.find_all('div', {'class': 'item-news'})
    urls_news = []
    for div in divs:
        url_pars = div.find('div', {'class': 'post-body'})
        url = url_pars.find('a').get('href')
        urls_news.append(url)
  
    return urls_news

# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Заголовок
    title = soup.find('h1', {'class': 'post-title'}).get_text(strip=True)
    
    # Описание
    content = soup.find('div', {'class': 'post-body video-rec'})
    text = content.get_text()
    
    # Время
    date_div = soup.find('div', {'class': 'data-post'})
     # Извлечение времени (текст до тега <span>)
    time = date_div.contents[0].strip()  # contents[0] возвращает первый текстовый элемент
    # Извлечение даты (текст внутри тега <span>)
    date = date_div.find('span').text.strip()
    
    return f"\n\nВремя: {time} {date}\nЗаголовок: {title}\nОписание:\n{text}"


# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result05.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами