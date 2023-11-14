"""
Here is a simple web browser that is looping constantly unless you ask it to "quit", if the URL doesn't have "https://" it will add it for the browser to work.
"""
import requests
import bs4


while True: # The "True" tells Python to always try to loop.
    url = input("Enter a URL (or 'quit' to exit): ")
    if url.lower().strip() == "quit":
        break
    if "https://" not in url: 
        url = "https://" + url 
    try:
        response =  requests.get(url)
        response.raise_for_status()  # Raise an Error for bad responses
        #print(response.content)
        html_doc = response.content
        soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    
        # Find all <a> elements and print code
        all_links = soup.find_all("a")
        for link in all_links:
            print(link)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    #print(soup.prettify())

# Output:

# <!DOCTYPE html>
# <html>
#   <body>
#     Hello, World!
#   </body>
# </html>
