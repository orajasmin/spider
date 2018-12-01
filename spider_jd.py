from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
import time

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 5)
KEYWORD = '跑步鞋'

def get_page(page):
	
	url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % quote(KEYWORD)
	browser.get(url)

	if page > 1:
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage input.input-txt')))
		input.clear()
		input.send_keys(page)
		
		
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage a.btn.btn-default')))
		submit.click()

	# for i in range(8):
	# 	str_js = 'var step = document.body.scrollHeight / 8; window.scrollTo(0, step * %d)' % (i + 1)
	# 	browser.execute_script(str_js)
	# 	time.sleep(1)

	page_source = browser.page_source
	return page_source

def parse_page(page_source):
	pass

def main():
	for page in range(100):
		print(page)
		page_source = get_page(page + 1)
		parse_page(page_source)

if __name__ == '__main__':
	main()