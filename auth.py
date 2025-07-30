import requests
from parser import get_token_from_html


def login(base_url, username, password):
    session = requests.Session()
    index_url = f"{base_url}/index.php"

    r = session.get(index_url)
    token = get_token_from_html(r.text)

    # Берётся из form с id='login_form'
    payload = {
        "pma_username": username,
        "pma_password": password,
        "server": 1,
        "target": "index.php",
    }

    if token:
        payload['token'] = token

    r = session.post(index_url, data=payload, allow_redirects=True)
    if 'pma_username' in r.text:
        raise Exception("Не удалось авторизоваться")

    token = get_token_from_html(r.text)
    return session, token, r.text


if __name__ == "__main__":
    with open("test/sample_login.html", "r", encoding="utf-8") as f:
        html = f.read()
        token = login('http://185.244.219.162/phpmyadmin', 'test', 'JHFBdsyf2eg8*')
        print("res:", token)

