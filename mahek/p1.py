import requests
from bs4 import BeautifulSoup,Comment
import re

url = "https://law.justia.com/codes/ohio/2021/title-13/chapter-1349/section-1349-61/"

response = requests.get(url)

if response.status_code == 200:
    print("Successfully fetched the data!") 
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    