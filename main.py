"""
Here is a simple web browser that is looping constantly unless you ask it to "quit", if the URL doesn't have "https://" it will add it for the browser to work.
"""
import requests


while True: # The "True" tells Python to always try to loop.
    url = input("Enter a URL (or 'quit' to exit): ")
    if url.lower().strip() == "quit":
        break
    if "https://" not in url: 
        url = "https://" + url 
    response =  requests.get(url)
    print(response.content)
