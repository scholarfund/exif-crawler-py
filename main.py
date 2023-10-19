"""
Here is a simple web browser that is looping constantly unless you ask it to "quit", if the URL doesn't have "https://" it will add it for the browser to work.
"""



while True: # The "True" tells Python to always try to loop.
    url = input("Enter a URL (or 'quit' to exit): ")
    if url.lower() == "quit":
        break
    if "https://" not in url: 
        url = "https://" + url 
    import requests
    response =  requests.get(url)
    print(requests)
    print(response.content)
