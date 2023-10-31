# Roadmap
---

- **Local imports**: Allows the importing of local files
```
import "local/file"
file.func()
```
- **Importing items**: Import specific items from a library
```
import "pause" from "time"
```
- **Repeat until**: Repeats a code block until a condition is met, like a while statement
```
x = 10
repeat {
    x = x - 1
} until x == 0
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
- **Struct functions**: Define functions after the struct definition
```
struct Vector2 {
    float x
    float y
}

func Vector2.string() {
    return to_string(self.x) + ', ' + to_string(self.y)
}

v = new Vector2(0, 0)
print(v.string())
```
- **Function expressions (lambdas)**: Concise way to define nameless functions meant to be used once
```
f = (x) => {
    print(x)
}

f(10)

print((x) => {
    return
}(10))
```
- **Optional chaining**: Safely accessing properties on potentially nil values
```
print(runtime.env.get("my_string")?.lower())
```
