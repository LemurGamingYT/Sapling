# Roadmap
---

- **Html support**: HTML parser support and the ability to build HTML.
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
- **Error Handling**: Use the 'try' and 'catch' keyword to catch errors.
```
try {
    print(2 / 0)
} catch TypeError {
    print("Caught division by zero error")
}
```
- **Classes**: Use the 'class' keyword to define a class - OOP (object-oriented-programming).
```
class Animal {
    func init() {
        self.name = "Animal"
    }

    func speak() {
        print("I am an " + self.name)
    }
}

class Dog <- Animal {
    func override init() {
        self.name = "Dog"
    }
}

dog = new Dog()
dog.speak()
```
- **Reference Parameters**: (a possible feature because I'm not sure how this would be implemented) pass parameters by reference, anything changed in the function will be changed outside of the function, identical to mutable parameters.
```
func test(int &x) {
    x = 10
    print(x)
}

y = 20
test(y)
print(y)
```
- **Events/Signals**: Bind a function to an event when something happens.
```
int x = 10

func x.on_change(int new_value) {
    print("x Changed value!")
}

print(x)
x = 25
```
- **Async/Await**: Asynchronus operations.
```
async func slow_task() {
    print("I'm slowwwwwwwww.......")
    print("Still waiitinnggggg.......")
    print("Loading game...............")

    print("Returning output...")
    return 0
}

async func test() {
    out1 = await slow_task()
    out2 = await slow_task()
}
```
- **String interpolation**: Easier string concatenation
```
x = 20
print($"My luckiest number is {x}")
print($"It's also {x - 5}")
```
