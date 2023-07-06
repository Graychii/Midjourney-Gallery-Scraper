from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import requests
from PIL import Image
import os 





desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

options = webdriver.ChromeOptions()

options.add_argument('headless')

options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome()

i = 0

driver.get("https://www.midjourney.com/showcase/recent/")
cookie = open('__cf_bm.txt').read()
_ga = open('_ga.txt').read()
_ga_Q0DQ5L7K0D = open('_ga_Q0DQ5L7K0D.txt').read()

time.sleep(10)

logs = driver.get_log("performance")

with open("network_log.json", "w", encoding="utf-8") as f:
	f.write("[")
  
        # Iterates every logs and parses it using JSON
	for log in logs:
		network_log = json.loads(log["message"])["message"]
		if("Network.response" in network_log["method"]
		or "Network.request" in network_log["method"]
		or "Network.webSocket" in network_log["method"]):
			f.write(json.dumps(network_log)+",")
  
print("Quitting Selenium WebDriver")
driver.quit()


images_links = []
base_url = 'https://cdn.midjourney.com'
json_file_path = "network_log.json"
with open(json_file_path, "r", encoding="utf-8") as f:
	x = f.read()
	x = x[::-1]
	x = ']' + x[1:]
	x = x[::-1]
	logs = json.loads(x)
for log in logs:

	try:
		if '.webp' in log['params']['headers'][':path']:
			images_links.append(log['params']['headers'][':path'])
	except Exception as e:
		a = 1
for image in images_links:
	url = base_url + image
	if len(url) == 78:
		headers = {'Cookie':f'_ga={_ga}; __cf_bm={cookie}; _ga_Q0DQ5L7K0D={_ga_Q0DQ5L7K0D}'
	,'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
	}
		print(url)
		try :
			r = requests.get(url, headers=headers, allow_redirects=True)
			print(r)
			if r.status_code == 200:
				open(f'test.webp', 'wb').write(r.content)
				im = Image.open('test.webp').convert('RGB')
				im.save(f'./images/image{i}.png', 'png')

				i+=1

		except Exception as e :
			a = 1



  
