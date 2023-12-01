"""
Here is a simple web browser that is looping constantly unless you ask it to "quit", if the URL doesn't have "https://" it will add it for the browser to work.
"""
import requests
import bs4
from urllib.parse import urljoin


def get_valid_url():
    while True: # The "True" tells Python to always try to loop.
        url = input("Enter a URL (or 'quit' to exit): ")
        if url.lower().strip() == "quit":
            return None
        if "https://" not in url: 
            url = "https://" + url 
        return url
    
def print_absolute_image_urls(url):
    try:
        response =  requests.get(url)
        response.raise_for_status()  # Raise an Error for bad responses
        #print(response.content)
        html_doc = response.content
        soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    
        # Find all <img> elements
        all_images = soup.find_all("img")
        
        # Print absolute URLs for image sources
        for img in all_images:
            src = img.get("src")
            absolute_url = urljoin(url, src)
            print(absolute_url)
        

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    while True:
        url = get_valid_url()
        if url is None:
            break

        print_absolute_image_urls(url)

if __name__ == "__main__":
    main()
    
    #print(soup.prettify())

# Output:

# <!DOCTYPE html>
# <html>
#   <body>
#     Hello, World!
#   </body>
# </html>
