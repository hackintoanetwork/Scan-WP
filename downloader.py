import concurrent.futures
import os
import requests
from bs4 import BeautifulSoup
import string

colors = [
    '\033[91m', # RED
    '\033[92m', # GREEN
    '\033[93m', # YELLOW
    '\033[94m', # BLUE
    '\033[95m', # MAGENTA
    '\033[96m', # CYAN
    '\033[90m', # DARK GRAY
    '\033[97m', # WHITE
    '\033[91m', # LIGHT RED
    '\033[92m'  # LIGHT GREEN
]

RESET = '\033[0m'

save_dir = "/Users/sehyoung/Downloads"

def get_existing_folders(save_dir):
    existing_folders = []
    for folder_name in os.listdir(save_dir):
        if os.path.isdir(os.path.join(save_dir, folder_name)):
            existing_folders.append(folder_name)
    return existing_folders

def download_plugin(link, existing_folders):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    download_link = soup.find('a', {'class': 'plugin-download button download-button button-large'})['href']

    file_name = download_link.split('/')[-1]
    folder_name = file_name.rsplit('.', 1)[0]

    if folder_name in existing_folders:
        print(f"Skipping {folder_name} as it already exists.")
        return 0

    save_path = os.path.join(save_dir, file_name)
    with open(save_path, 'wb') as f:
        f.write(requests.get(download_link).content)
    print('Downloaded:', file_name)

def download_plugins_on_page(page_num, existing_folders, target):
    base_url = "https://ko.wordpress.org/plugins/search/{}/page/".format(target)
    url = base_url + str(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if not soup.find_all('h3', {'class': 'entry-title'}):
        return []

    plugins = soup.find_all('h3', {'class': 'entry-title'})
    links = [plugin.find('a')['href'] for plugin in plugins]

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = [executor.submit(download_plugin, link, existing_folders) for link in links]
        for result in concurrent.futures.as_completed(results):
            pass
    return links

def download_plugins_for_target(target, existing_folders, color_code):
    page_num = 1

    while True:
        links = download_plugins_on_page(page_num, existing_folders, target)
        if not links:
            break
        print(f'{color_code}Downloaded {len(links)} plugins from page {page_num} for {target}.{RESET}')
        page_num += 1
        if page_num > 50:
            break

if __name__ == "__main__":
    targets = input(">> ").split()[:10]  # Limit to 10 targets
    existing_folders = get_existing_folders(save_dir)

    print("아래의 키워드에 대한 플러그인을 다운로드 합니다.")
    print("-------------------------------------------------")
    for i, target in enumerate(targets):
        print(f'{i+1}. {colors[i % len(colors)]}{target}{RESET}')
    print("-------------------------------------------------\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = [executor.submit(download_plugins_for_target, target, existing_folders, colors[i % len(colors)]) for i, target in enumerate(targets)]
        for result in concurrent.futures.as_completed(results):
            pass