"""
Here is a simple web browser that is looping constantly unless you ask it to "quit", if the URL doesn't have "https://" it will add it for the browser to work.
"""
import requests
import bs4
from PIL import Image
import io
import urllib

def get_valid_url():
    while True:
        url = input("Enter a URL (or 'quit' to exit): ").strip().lower()
        if url == "quit":
            return None
        if "https://" not in url:
            url = "https://" + url
        return url

def download_image_as_bytes(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def open_bytes_as_image(image_data):
    try:
        image_stream = io.BytesIO(image_data)
        return Image.open(image_stream)
    except Exception as e:
        print(f"Error opening image as bytes: {e}")
        return None
    
def get_file_extension(file_path):
    """
    Split the file extension (such as "jpg", "svg", "html", "docx") from the
    rest of the file path. Return the extension, lowercased, with no leading
    "." at the beginning. (For example: "jpg", not "JPG" or ".jpg".)
    """
    my_split_string = file_path.split(".")

    return my_split_string[-1]
    
def list_exif_tags(image):
    exif_mapping = image.getexif()
    if exif_mapping is not None:
        tag_ids = list(exif_mapping.keys()) 
        return tag_ids
    else:
        return []
    
def get_absolute_image_urls(page_url):
    """
    Fetch an HTML page, parse it, identify <img> tags, and return a list
    containing the absolute URLs of their `src` attributes.
    """

    response = requests.get(page_url)  # Make HTTP request to server
    response.raise_for_status()  # Raise an Error for bad responses
    html_doc = response.content

    soup = bs4.BeautifulSoup(html_doc, "html.parser")  # Parse HTML tags from response
    all_images = soup.find_all("img")  # Extract all <img src="....."> tags

    all_urls = []
    for image in all_images:
        src = image.get("src")
        absolute_url = urllib.parse.urljoin(page_url, src)
        all_urls.append(absolute_url)  # Add URL to the list that will be returned

    return all_urls

def is_approved_origin(url):
    """
    Returns False if URL's origin is not in an explicitly approved list.
    Checking this helps mitigate server side request forgery, in case a page
    being scanned references a URL that should only be accessible from within
    a protected network boundary.
    """
    approved_origins = [
        "https://www.scholarfundwa.org",
        "https://assets-global.website-files.com",
    ]
    parsed_url = urllib.parse.urlparse(url)
    url_origin = f"{parsed_url.scheme}://{parsed_url.netloc}"
    for approved_origin in approved_origins:
        if url_origin == approved_origin:
            return True
    return False

def scan_page(page_url):
    """
    Fetch an HTML page and scan it for images with EXIF metadata.
    """

    image_urls = get_absolute_image_urls(page_url)
    image_urls = [url for url in image_urls if is_approved_origin(url)]
    print("All image URLS:", image_urls)
    print()  # Print blank line for clarity

    for image_url in image_urls:
        if get_file_extension(image_url) != "svg":
            print("Image URL:", image_url)

            raw_data = download_image_as_bytes(image_url)
            print("Raw image data:", raw_data[:64], "...")  # Print first 64 bytes

            image = open_bytes_as_image(raw_data)
            print("Decoded image size (pixels):", image.size)

            exif_tags = list_exif_tags(image)
            print("EXIF tags:", exif_tags)

            if 0x8825 in exif_tags:  # Check for GPS metadata tag
                message = generate_slack_message(image_url, page_url)
                post_to_slack(message)

            print()  # Print blank line for clarity

def normalize_url(url):
    """
    Return a standardized URL, adding the "https://" scheme to the beginning if
    needed.
    """

    url = url.strip()  # Remove leading and trailing spaces

    # Prepend scheme to URL if missing
    if not url.startswith("https://"):
        url = "https://" + url

    return url       

def generate_slack_message(image_url, page_url):
    """
    Generate a Slack message when GPS metadata is found in an image URL.
    """
    return (
        ":map: I'm crawling the website and noticed that the image "
        f"{image_url} on page {page_url} might have unwanted EXIF metadata embedded, "
        "possibly including geographic location."
    )

def post_to_slack(message):
    """
    Post a message to Slack using Zapier's webhook URL.
    """
    webhook_url = "https://hooks.zapier.com/hooks/catch/9954195/bvr7oxh/"
    requests.post(webhook_url, json={"message": message})   

def main():
    """
    Main function to interact with the user and scan web pages.
    """
    page_url = "https://www.scholarfundwa.org/about"
    scan_page(page_url)

if __name__ == "__main__":
    main()
