"""
Prints the number of pages crawled. (Does not have any crawling code,
so the number is always 0.)
"""

import requests



print ("Using requests version:", requests.__version__)

num_pages = 0
print("Found", num_pages, "pages.")

response =  requests.get("https://www.scholarfundwa.org/")
print(response.content)
