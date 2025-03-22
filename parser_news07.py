import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://rus-kostroma.ru/'


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
    
    news_blocks = soup.find_all('div', class_='col-xs-16 col-sm-8 col-md-9')
    urls_news = []
    for block in news_blocks:
        # Находим все теги <a> внутри блока, исключая теги внутри news__tags
        for tag in block.find_all('a'):
            if not tag.find_parent('div', class_='news__tags'):
                link = tag.get('href')
                result_url = f'https://rus-kostroma.ru{link}'
                urls_news.append(result_url)
  
    return urls_news

# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Заголовок
    title = soup.find('h1', {'class': 'd-news__h1'}).get_text()
    # Время
    time = soup.find('span', {'class': 'info'}).get_text()
    # Описание
    content = soup.find('div', {'class': 'd-news__detail-text'})
    descriptoin = content.find_all('p')
    res_text = ''
    for el in descriptoin:
        res_text += f"{el.get_text(strip=True)}\n"
    
    return f"\n\nВремя: {time}\nЗаголовок: {title}\nОписание:\n{res_text}"

# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result07.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description[1:]:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами