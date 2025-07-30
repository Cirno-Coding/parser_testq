import config
from auth import login
from parser import find_table_browse_urs, parse_results_table


def print_table(header, data_table):
    res = ''
    str_rows = [[str(item) for item in row] for row in data_table]
    str_headers = [str(header) for header in header]
    all_data = [str_headers] + str_rows

    col_widths = []
    for col_idx in range(len(header)):
        max_width = max(len(row[col_idx]) for row in all_data)
        col_widths.append(max_width)

    div_line = '+-' + '-+-'.join('-' * width for width in col_widths) + '-+\n'
    res += div_line

    header_line = '| ' + ' |'.join(
        f"{str_headers[i]:<{col_widths[i]}}" for i in range(len(header))
    ) + '  |\n'
    res += header_line
    res += div_line

    for row in str_rows:
        row_line = '| ' + ' | '.join(
            f"{row[i]:<{col_widths[i]}}" for i in range(len(header))
        ) + ' |\n'
        res += row_line
    res += div_line
    return res


def main():
    session, token, home_html = login(config.BASE_URL, config.USERNAME, config.PASSWORD)

    browse_url = find_table_browse_urs(home_html, config.BASE_URL, config.DEFAULT_DB, config.DEFAULT_TABLE)
    if not browse_url:
        raise Exception(f"Не удалось найти ссылку на таблицу {config.DEFAULT_TABLE}")

    html = session.get(browse_url).text

    rows, headers = parse_results_table(html)

    print(f"Таблица {config.DEFAULT_TABLE}:")
    print(print_table(headers, rows))


if __name__ == '__main__':
    main()

