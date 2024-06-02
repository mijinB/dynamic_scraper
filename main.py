from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

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

print(job_db)
print(len(job_db))