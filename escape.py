import markupsafe
import html

#unescaped_html = '<a href="https://example.com">Click Me</a>'
#escaped_html = html.escape(unescaped_html)

#print(escaped_html)
while True:
    user_input = input("Enter some text (or type 'quit' to exit): ")

    if user_input.lower().strip() == 'quit':
        break

    escaped_html = markupsafe.escape(user_input)
    print("escaped html:", escaped_html)
   