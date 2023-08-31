import os
import re
import requests
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup

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
    with open('/Users/sehyoung/WordPress/Fuzzer/analysis-done.txt', 'r') as file:
        content = file.read()
        if plugin_name in content:
            return False
        else:
            return True

def find_php_files(directory):
    return [f for f in Path(directory).glob('**/*.php') if f.is_file()]

def detect_vulnerable_code(file_path):
    with open(file_path, 'r', encoding='latin1') as file:
        content = file.readlines()

    input_pattern = r'\$(\w+)\s*=\s*(?:\$_GET|\$_REQUEST|\$_POST)\s*\[(?:\'|\")(\w+)(?:\'|\")\]'
    output_pattern = r'echo\s*\$'

    vulnerable_variables = dict()

    for line_no, line in enumerate(content, start=1):
        if not line.strip().startswith('//') and not line.strip().startswith('/*') and not line.strip().startswith('*') and not line.strip().startswith('*/'):  # Ignore commented lines
            request_matches = re.finditer(input_pattern, line)
            for match in request_matches:
                var_name = match.group(1)
                vulnerable_variables[var_name] = (line_no, line.strip())

    vulnerable_lines = []

    for var_name, (input_line_no, input_line) in vulnerable_variables.items():
        for line_no, line in enumerate(content, start=1):
            if not line.strip().startswith('//') and not line.strip().startswith('/*') and not line.strip().startswith('*') and not line.strip().startswith('*/'):  # Ignore commented lines
                if re.search(f'{output_pattern}{var_name}', line):
                    vulnerable_lines.append((input_line_no, input_line, line_no, line.strip()))
                    break

    return vulnerable_lines

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

def main(directory):
    php_files = find_php_files(directory)
    install = 1000
    for file_path in php_files:
        vulnerable_lines = detect_vulnerable_code(file_path)
        if vulnerable_lines:
            plugin_name = f"{file_path}".split('/')[4]
            url, last_updated_day, installations_count = plugin_meta(plugin_name)
            if duplicate_check(plugin_name):
                if plugin_installations(installations_count) >= int(install):
                    for input_line_no, input_line, output_line_no, output_line in vulnerable_lines:
                        if output_line_no > input_line_no:
                            echo_start_index = output_line.find('echo')
                            semicolon_index = output_line.find(';', echo_start_index)
                            output_line_colored = output_line[:echo_start_index] + ConsoleColor.OKBLUE + output_line[echo_start_index:semicolon_index + 1] + ConsoleColor.ENDC + output_line[semicolon_index + 1:]
                            
                            print("--------------------------------------------------------------------------------------------")
                            print()
                            print(ConsoleColor.OKGREEN + "Vulnerable code detected in : " + ConsoleColor.ENDC + f"{file_path}")
                            print()
                            print(ConsoleColor.WARNING + "[+] Plugin URL : " + ConsoleColor.ENDC + f"{url}")
                            print(ConsoleColor.WARNING + "[+] Last updated : " + ConsoleColor.ENDC + f"{last_updated_day}")
                            print(ConsoleColor.WARNING + "[+] Active installations : " + ConsoleColor.ENDC + f"{installations_count}")
                            print()
                            print(ConsoleColor.OKCYAN + f"Input Line {input_line_no} : \n " + ConsoleColor.ENDC + f"{input_line}")
                            print()
                            print(ConsoleColor.OKCYAN + f"Output Line {output_line_no} : \n " + ConsoleColor.ENDC + f"{output_line_colored}")
                            print()

if __name__ == '__main__':
    directory = '/Users/sehyoung/Downloads' # 플러그인 다운로드 디렉터리로 수정
    try:
        zip_extract(directory)
        main(directory)
    except:
        exit()
