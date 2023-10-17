"""
Here is a simple web browser that is looping constantly, if the URL doesn't have "https://" it will add it for the browser to work.
"""



while True: # The "True" tells Python to always try to loop.
    url = input("Enter a URL: ")
    if "https://" not in url: 
        url = "https://" + url 
    import requests
    response =  requests.get(url)
    print(requests)
    print(response.content)
