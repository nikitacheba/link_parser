# link_parser
Простой парсер ссылок с выгрузкой в ЬД
Парсер собирает ссылки на статьи только с сайта habr.com и только с одной страницы.
Если нужно собирать с нескольких страниц - нужна функция пагинации:
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all(
        'a', class_='toggle-menu__item-link toggle-menu__item-link_pagination')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
С соответствующим изменением фунции parse

