import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://gtrk-kostroma.ru/'


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
    
    section = soup.find('div', {'class': 'row news-list news-list--lenta'})
    divs = section.find_all('div', {'class': 'col col-12'})
    
    urls_news = []
    for div in divs:
        url_pars = div.find('a')
        schema = 'https://gtrk-kostroma.ru'
        result_url = f'{schema}{url_pars.get('href')}'
        urls_news.append(result_url)
  
    return urls_news


# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Заголовок
    title = soup.find('h1', {'class': 'text-align-center'}).get_text(strip=True)
    
    # Заголовок к описанию 
    elem_h1 = soup.find('div', {'class': 'description-block description-block--blue'}).get_text(strip=True)
    # Описание
    detail_text = soup.find_all('div', {'class': 'detail__text'})
    description = detail_text[-1]
    text = description.get_text(strip=True) 
    
    # Время
    time = soup.find('span', class_='detail__date').get_text(strip=True)
    
    return f"\n\nВремя: {time}\nЗаголовок: {title}\nОписание:\n{elem_h1}\n{text}"

# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)
# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result04.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами