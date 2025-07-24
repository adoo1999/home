
from bs4 import BeautifulSoup
import requests
from git import Repo
import time

def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # 에러 발생 시 예외 처리
        ip = response.json().get("ip")
        return ip
    except Exception as e:
        print("외부 IP를 가져오는 중 오류 발생:", e)
        return ""

prevIp = "";

while True:
    ip = get_external_ip();

    if ip == prevIp:
        time.sleep(60)
        continue
    
    # 1. index.html 파일 읽기
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 2. <a name="dtrader"> 태그 찾기
    a_tag = soup.find("a", attrs={"name": "dtrader"})

    # 3. href 변경
    if a_tag:
        url = "http://" + ip
        a_tag['href'] = url
        print(url + " 링크 수정 완료.")
    else:
        print("name='dtrader'인 <a> 태그를 찾을 수 없습니다.")

    # 4. 다시 index.html에 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))
        
    repo = Repo(".")
    repo.git.add("index.html")
    repo.index.commit("Add index.html")
    origin = repo.remote(name="origin")
    origin.push()
    
    prevIp = ip