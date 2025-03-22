import requests
from bs4 import BeautifulSoup
from config import headers, proxy_auth

url = 'https://www.kostroma.kp.ru'


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
    section = soup.find('div', {'class': 'sc-k5zf9p-13 fsrrpT'})
    links = section.find_all('a', {'class': 'sc-k5zf9p-3 dqylVG'})
    
    urls_news = []
    for a in links:
        schema = 'https://www.kostroma.kp.ru'
        result_url = f'{schema}{a.get('href')}'
        urls_news.append(result_url)  
    return urls_news


# Функция для извлечения данных из страницы новости
def extract_article_data(html):
    soup = BeautifulSoup(html, 'lxml')
    
    # Заголовок
    title = soup.find('h1', {'class': 'sc-j7em19-3 eyeguj'}).get_text(strip=True)
    
    # Описание
    content = soup.find('div', {'class': 'sc-1wayp1z-0 sc-1wayp1z-5 gwmrBl chEeRL'})
    content_text = content.find_all('p', {'class': 'sc-1wayp1z-16 dqbiXu'})
    text = '\n'.join(message.text for message in content_text[0:-1])
    
    # Время
    time = soup.find('span', {'class': 'sc-j7em19-1 dtkLMY'}).get_text(strip=True)
    return f"\n\nВремя: {time}\nЗаголовок: {title}\nОписание:\n{text}"

# Получаем HTML главной страницы
main_page_html = fetch_page(url, headers, proxy_auth)

# Извлекаем ссылки на новости
links_news_description = extract_links(main_page_html)

# Создаем файл и записываем результат
with open('pars_result02.txt', 'w', encoding='utf-8') as f:
    # Обрабатываем каждую новость
    for link in links_news_description:
        article_html = fetch_page(link, headers, proxy_auth)
        # Извлекаем данные и записываем в файл
        article_data = extract_article_data(article_html)
        f.write(article_data)
        f.write("\n" + "-" * 150 + "\n")  # Разделитель между постами