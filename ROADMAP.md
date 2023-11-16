# Roadmap
---

- **Importing items**: Import specific items from a library
```
import "pause" from "time"
```
- **Html support**: HTML parser support and the ability to build HTML
```
html = "<html>
    <body>
        <h1>Hello world!</h1>
    </body>
</html>
"

parsed = parsers.html.parse_text(html)
print(parsed)
{
    HTML:
        Body:
            H1:
                text: "Hello world!"
}
```
- **Error Handling**: Use the 'try' and 'catch' keyword to catch errors
```
try {
    print(2 / 0)
} catch TypeError {
    print("Caught division by zero error")
}
```
