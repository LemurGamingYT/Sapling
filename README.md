<p align="center">
    <img src="icon.ico" width="128">
</p>

# Sapling
 A bytecode VM made in Python


## How to run
There are two ways to run Sapling.

1. Use the .exe file
    1. Clone the repository
        - Optionally add 'bin' to PATH
    2. Run `sapling [file]` (replace `[file]` with the file you want to run)
2. Run using Python
    1. Install python >3.12.0
        - Add python to PATH
        - Install requirements.txt with pip: `pip install -r requirements.txt`
    2. Run `python [file]` (replace `[file]` with the file you want to run)


### Roadmap
- **Local imports**: Allows the importing of local files
```
import "local/file"
file.func()
```
- **Importing items**: Import specific items from a library
```
import "pause" from "time"
```
- **Repeat until**: Repeats a code block until a condition is met, like a white statement
```
x = 10
repeat {
    x = x - 1
} until x == 0
```
- **Html support**: HTML parser support and ability to build HTML
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
- **Dictionary support**: Currently, the dictionary object is hidden away and only accessible by parsers.json
```
d = {"key": "value"}
print(d)
{"key": "value"}
```
