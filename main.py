from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

for x in range(4):
  time.sleep(5)

  page.keyboard.down("End")

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__FqChn")

job_db = []

for job in jobs:
  link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
  title = job.find("strong", class_="JobCard_title__ddkwM").text
  company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text
  reward = job.find("span", class_="JobCard_reward__sdyHn").text
  job = {
    "title": title,
    "company": company_name,
    "reward": reward,
    "link": link,
  }
  job_db.append(job)

# .csv(comma separated values) = 쉼표로 나누어진 값
# Excel 파일과 비슷하지만 더 범용성이 있다. (Excel이나 MacOS의 Pages처럼 다양한 방법으로 읽을 수 있다.)
# csv 파일 미리보기 확장자 = Excel Viewer
file = open("jobs.csv", "w", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Reword", "Link"])

for job in job_db:
  writer.writerow(job.values())

file.close()