from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def get_token_from_html(html, current_url=None):
    soup = BeautifulSoup(html, "html.parser")
    token_input = soup.select_one("input[name=token]")
    if token_input:
        return token_input.get("value")

    if current_url:
        qs = parse_qs(urlparse(current_url).query)
        if "token" in qs:
            return qs["token"][0]

    return None


def find_table_browse_urs(html, base_url, db_name, table_name):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        if f"table={table_name}" in a['href']:
            return f"{base_url}/{a['href']}"
    return None


def parse_results_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', class_='table_results')

    headers = [th.find('a').text.strip() for th in table.thead.find_all('th')][1:]
    if '   1' in headers[0]:
        headers[0] = headers[0].replace('   1', '').strip()

    rows = []
    for tr in table.tbody.find_all('tr'):
        tmp = [td.text.strip() for td in tr.find_all("td")]
        rows.append(tmp[len(tmp) - len(headers):])

    return rows, headers


if __name__ == "__main__":
    with open("test/sample_table.html", "r", encoding="utf-8") as f:
        html = f.read()
        token = parse_results_table(html)
        print("res:", token)
