def calculator():
    print("=== Simple Python Calculator ===")
    print("Supported operations: +  -  *  /  %  **")
    print("Type 'exit' at any time to quit.\n")

    while True:
        try:
            
            num1 = input("Enter first number: ")
            if num1.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break

            num1 = float(num1)

            operator = input("Enter operator (+, -, *, /, %, **): ")
            if operator.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break

            num2 = input("Enter second number: ")
            if num2.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break

            num2 = float(num2)

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero.")
                result = num1 / num2
            elif operator == '%':
                if num2 == 0:
                    raise ZeroDivisionError("Cannot modulo by zero.")
                result = num1 % num2
            elif operator == '**':
                result = num1 ** num2
            else:
                raise ValueError("Invalid operator entered.")

            print(f"Result: {result}\n")

        except ValueError as ve:
            print(f"Error: Invalid input. {ve}\n")
        except ZeroDivisionError as zde:
            print(f"Error: {zde}\n")
        except Exception as e:
            print(f"Unexpected error: {e}\n")


# if __name__ == "__main__":
#     calculator()