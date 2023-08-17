import requests
from bs4 import BeautifulSoup
import json


url = 'http://127.0.0.1:5500/index.html'

response = requests.get(url)
bs = BeautifulSoup(response.text, "lxml")
temp = bs.find('pre')

print(temp.text)