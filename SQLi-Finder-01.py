import os
import re
import requests
from bs4 import BeautifulSoup

method_variable = r"((?:(\$[a-zA-Z_\x7f-\xff](?:[a-zA-Z0-9_\x7f-\xff]+)?)(?:[\s\t]+)=(?:[\s\t]+))+.*(?:\$_GET|$_REQUEST)\[.*\].*(?:;)?)"
sql_query = r"\$wpdb->(?:query|get_var|get_row|get_col|get_results|insert|update|delete)\s*\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)"
sql_query_with_request_vars = r"(?=.*(?:\$_GET|$_POST|$_REQUEST)\[.*\])" + sql_query

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

def plugin_installations(installations_count):
    numbers = re.findall(r'\d+', installations_count)
    active_installations_number = int(''.join(numbers))
    return active_installations_number

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

def find_sql_queries_in_files(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.php'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='latin1') as f:
                    file_content = f.read()

                    method_variable_search = re.search(method_variable, file_content)
                    sql_query_method_search = re.search(sql_query_with_request_vars, file_content)

                    plugin_name = f"{file_path}".split('/')[4]

                    if method_variable_search and sql_query_method_search:
                        if ('sanitize_text_field(' not in method_variable_search.group(0)) and ('esc_sql(' not in method_variable_search.group(0)) and ('$wpdb->prepare(' not in method_variable_search.group(0)) and ('sanitize_key(' not in method_variable_search.group(0)):
                            url, last_updated_day, installations_count = plugin_meta(plugin_name)
                            if plugin_installations(installations_count) > 900:
                                print("----------------------------------------------------------------------------------------------------")
                                print()
                                print(ConsoleColor.OKGREEN + "SQL query found in:" + ConsoleColor.ENDC + f"{file_path}")
                                print()
                                print(ConsoleColor.WARNING + "[+] Plugin URL : " + ConsoleColor.ENDC + f"{url}")
                                print(ConsoleColor.WARNING + "[+] Last updated : " + ConsoleColor.ENDC + f"{last_updated_day}")
                                print(ConsoleColor.WARNING + "[+] Active installations : " + ConsoleColor.ENDC + f"{installations_count}")
                                print()
                                if sql_query_method_search:
                                    print(ConsoleColor.OKCYAN + "Matched sql_query_method:\n", ConsoleColor.ENDC, sql_query_method_search.group(0))
                                print()


if __name__ == "__main__":
    try:
        wordpress_path = "/Users/user/Downloads" # change here
        find_sql_queries_in_files(wordpress_path)
    except:
        exit()
