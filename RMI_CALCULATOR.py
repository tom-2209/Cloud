NOTE #############
first run this commend on the terminal to install pyro4
python -m pip install Pyro4

#SERVER CODE
import Pyro4

@Pyro4.expose
class Calculator:
    def add_numbers(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

daemon = Pyro4.Daemon()
uri = daemon.register(Calculator)

print("Calculator server is running...")
print("Server URI:", uri)

daemon.requestLoop()



###CLIENT CODE
import Pyro4

uri = input("Enter the server URI: ")
uri = uri.strip()

print("URI received:", repr(uri))

try:
    parsed_uri = Pyro4.core.URI(uri)
    print("URI format is valid!")

    calculator = Pyro4.Proxy(parsed_uri)

    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    print("Addition:", calculator.add_numbers(a, b))
    print("Multiplication:", calculator.multiply(a, b))

    calculator._pyroRelease()

except Exception as e:
    print(type(e).__name__ + ":", e)

