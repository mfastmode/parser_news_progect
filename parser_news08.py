import requests
from bs4 import BeautifulSoup
from config_rus_proxy import headers, proxy_auth

# Сайт органов власти блочит прокси
url = 'https://adm44.ru/news/'


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
    news_blocks = soup.find_all('div', {'class': 'bx-newslist-container col-sm-6 col-md-4'})
    urls_news = []
    for block in news_blocks:
        div = block.find('div', {'class': 'bx-newslist-block'})
        link = div.find('a').get('href')
        res_url = f'https://adm44.ru{link}'
        urls_news.append(res_url)
        
    return urls_news

# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Главный заголовок
    title = soup.find('h1', {'class': 'article__title'}).get_text()
    # Время
    data = soup.find('span', {'class': 'article__date'}).get_text()
    time = soup.find('span', {'class': 'article__date article__date--time'}).get_text()
    # Заголовок к описанию 
    title_description = soup.find('p', {'class': 'article__preview'}).get_text()
    # Описание
    content = soup.find('div', {'class': 'article__text bvi-voice'})
    descriptoin = content.find_all('p')
    res_text = ''
    for el in descriptoin:
        res_text += f"{el.get_text(strip=True)}\n"
    
    return f"\n\nВремя: {data}{time}\nЗаголовок: {title}\nОписание:\n{title_description}\n{res_text}"

# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result08.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами