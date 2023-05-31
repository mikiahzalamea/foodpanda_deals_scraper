from bs4 import BeautifulSoup
import requests
import pandas
from playwright.sync_api import Playwright, sync_playwright
from playwright_stealth import stealth_sync
from playwright_recaptcha import recaptchav2

url = "https://www.foodpanda.ph/contents/deals"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    #stealth(context)
    # Set the user agent header to make the request more human-like
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Set the custom headers for the browser context
    context.set_extra_http_headers(headers)
    page = browser.new_page()

    stealth_sync(page)
    response = page.goto(url, wait_until="networkidle")
    try:
        with recaptchav2.SyncSolver(page) as solver:
            token = solver.solve_recaptcha()
            print(token)
    except:
        pass
    
    page.wait_for_load_state("networkidle")
    content = response.text()
    # Do something with the page
    browser.close()

soup = BeautifulSoup(content, "html.parser")

with open ("deals.html", "w") as file:
     file.write(str(soup.prettify()))

df_list = pandas.read_html("deals.html")

df_list[0]['code'] = df_list[0]['MECHANICS'].str.extract(r'Code:\s+(\w+)')
print(df_list[0])
# print(df)


