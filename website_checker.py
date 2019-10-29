import time
from urllib import request
from bs4 import BeautifulSoup  # Requires beautifulsoup4


website = 'https://de.wikipedia.org/wiki/Website'


def main():
    page_plain = get_website_text()
    while True:
        time.sleep(2)
        page = get_website_text()

        if not page_plain:
            page_plain = page
            continue

        if page != page_plain:
            changes = get_changes(page_plain, page)
            page_plain = page

            start_notification(changes)
            continue

        print('no changes')

    return 0


def get_website_text():
    # Retrieve text
    page = request.urlopen(website).read()
    soup = BeautifulSoup(page, features="html.parser")
    soup_text = soup.get_text()
    # print(soup_text)

    # Remove empty lines
    while '\n \n' in soup_text:
        soup_text = soup_text.replace('\n \n', '\n\n')
    while '\n\n' in soup_text:
        soup_text = soup_text.replace('\n\n', '\n')

    return soup_text


def get_changes(old, new):
    a = old.splitlines()
    b = new.splitlines()
    len_a = len(a)
    len_b = len(b)

    changes = []
    for i in range(max(len_a, len_b)):
        if i >= len_a:
            changes.append('[' + str(i) + '] ""   >   "' + b[i] + '"')
        elif i >= len_b:
            changes.append('[' + str(i) + '] "' + a[i] + '"   >   ""')
        elif a[i] != b[i]:
            changes.append('[' + str(i) + '] "' + a[i] + '"   >   "' + b[i] + '"')

    return changes


def start_notification(changes):
    print('\n'.join(changes))
    print('\n\n\n\n')


if __name__ == "__main__":
    main()