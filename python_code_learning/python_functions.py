print("Learning Functions in Python ")
# Function definition
def add(a,b):
    return a+b

print("Using the add function to add two numbers")
print("Enter First NUmber")
num1=int(input())
print("Enter Second number:")
num2=int(input())
result=add(num1,num2)
print("Result of addition:",result)

print("----------------------------------------")
print("\n")
print("Error Handling in Python")

try:
    a=10
    b=0
    result=a/b
    print("Result of division:",result)

except Exception as e:
    #print("Error: Division by zero is not allowed")
    print("Exception details:",e)
   # raise e
else:
    print("Division successful, no errors occurred")

finally:

    print("This block will always execute")