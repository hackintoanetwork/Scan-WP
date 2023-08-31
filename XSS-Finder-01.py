import os
import re
import zipfile
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class ConsoleColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def scan_file(file_contents, file_path):
    find_patterns_in_file(file_contents, file_path)

def walk(func, directory):
    with ThreadPoolExecutor(max_workers=1000) as executor:
        for directory, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(directory, filename)
                if filepath[-4:] == ".php":
                    with open(filepath, 'r', encoding='latin1') as file:
                        file_contents = file.read()
                        executor.submit(func, file_contents, filepath)

def plugin_meta(plugin_name):
    url = f"https://wordpress.org/plugins/{plugin_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    plugin_meta = soup.select_one("div.widget.plugin-meta")
    last_updated = plugin_meta.select_one("li:nth-of-type(2)")
    active_installations = plugin_meta.select_one("li:nth-of-type(3)")
    last_updated_day = last_updated.select_one("strong").text
    installations_count = active_installations.select_one("strong").text
    return url, last_updated_day, installations_count

def plugin_installations(installations_count):
    numbers = re.findall(r'\d+', installations_count)
    active_installations_number = int(''.join(numbers))
    return active_installations_number

def duplicate_check(plugin_name):
    with open('/Users/sehyoung/WordPress/Fuzzer/analysis_done.txt', 'r') as file:
        content = file.read()
        if plugin_name in content:
            return False
        else:
            return True

def find_patterns_in_file(file_contents, file_path):
    pattern = r"echo\s+\$?(?:_GET|_POST|_REQUEST)\[.*?\]"

    content_without_comments = re.sub(r'\/\/.*', '', file_contents)
    content_without_comments = re.sub(r'\/\*.*?\*\/', '', content_without_comments, flags=re.DOTALL)

    matches1 = [(m.start(), m.group()) for m in re.finditer(pattern, content_without_comments, re.IGNORECASE)]

    plugin_name = f"{file_path}".split('/')[4]
    
    if matches1:
        url, last_updated_day,installations_count = plugin_meta(plugin_name)
        if duplicate_check(plugin_name):
            if plugin_installations(installations_count) > 900:
                for start, match in matches1:
                    line_number = file_contents[:start].count('\n') + 1
                    echo_start_index = match.find('echo')
                    semicolon_index = match.find(';', echo_start_index)
                    match_colored = match[:echo_start_index] + ConsoleColor.OKBLUE + match[echo_start_index:semicolon_index + 1] + ConsoleColor.ENDC + match[semicolon_index + 1:]
                    print("--------------------------------------------------------------------------------------------")
                    print()
                    print(ConsoleColor.OKGREEN + "Vulnerable code detected in : " + ConsoleColor.ENDC + f"{file_path}")
                    print()
                    print(ConsoleColor.WARNING + "[+] Plugin URL : " + ConsoleColor.ENDC + f"{url}")
                    print(ConsoleColor.WARNING + "[+] Last updated : " + ConsoleColor.ENDC + f"{last_updated_day}")
                    print(ConsoleColor.WARNING + "[+] Active installations : " + ConsoleColor.ENDC + f"{installations_count}")
                    print()
                    print(ConsoleColor.OKCYAN + f"Output Line {line_number} :" + ConsoleColor.ENDC + f"\n {match_colored}")
                    print()

def zip_extract(directory):
    for file in os.listdir(directory):
        if file.endswith('.zip'):
            zip_file_path = os.path.join(directory, file)
            try:
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(directory)
                    print(ConsoleColor.OKGREEN + "[+] ZIP 파일 압축 해제 완료" + ConsoleColor.ENDC)
            except:
                continue
            os.remove(zip_file_path)
            print(ConsoleColor.WARNING + "[+] ZIP 파일 삭제 완로" + ConsoleColor.ENDC)

if __name__ == "__main__":
    directory = '/Users/sehyoung/Downloads' # 플러그인 다운로드 디렉터리로 수정
    zip_extract(directory)
    try:
        walk(scan_file,directory)
    except:
        exit()
