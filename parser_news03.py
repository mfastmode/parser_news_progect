import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://gorodok.city/default.aspx'


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
 
    table = soup.find('table', id='MainNews_dlNews')
    rows = table.find_all('tr')
    
    urls_news = []
    for row in rows:
        link = row.find('td').a.get('href')
        schema = 'https://gorodok.city'
        result_url = f'{schema}{link}'
        urls_news.append(result_url)  
        
    return urls_news

# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Заголовок
    title = soup.find('span', {'id': 'ctl12_ctl00_lTitle'}).get_text(strip=True)
    
    # Описание
    content = soup.find('span', id='ctl12_ctl00_lNews')
    content_text = content.find_all('div')
    text = '\n'.join(message.text for message in content_text)
    
    # Время
    time = soup.find('span', id='ctl12_ctl00_lData').get_text(strip=True)
    
    return f"\n\nВремя: {time}\nЗаголовок: {title}\nОписание:\n{text}"



# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result03.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами