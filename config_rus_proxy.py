# Например (как должны выглядить данные)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

headers = {
    'User-Agent': f'{user_agent}'
}

# Например (как должны выглядить данные)
login = 'vAbMvL'
password = '8jYaUq'
ip = '193.39.231.50'
port = '8000'

proxy_auth = {
    'http': f'http://{login}:{password}@{ip}:{port}',
    'https': f'http://{login}:{password}@{ip}:{port}'
}