print("Welcome")
name="Srividhya"
print("Hello",name)

#Data types

print("Learn about List")
fruits=["apple","banana","grapes"]
print(fruits)
# Add element to list
print("Add element to list")
fruits.append("orange")
print(fruits)
# Using index to access list element
print("Using index to access list element")
print(fruits[2])
#  delete element from list and add change to new element
print("replace element in list")
fruits[1]="mango"
print(fruits)
# remove element from list
print("remove element from list")
fruits.remove("apple")
print(fruits)
# length of list
print("length of list")
print(len(fruits))

print("---------------------------------------")
print("\n")
print("Learn about Tuple"  )
# Tuple is immutable
my_tuple=(10,20,30,40,50)
print(my_tuple)
# Accessing tuple element using index
print("Accessing tuple element using index")
print(my_tuple[3])
# length of tuple
print("length of tuple")
print(len(my_tuple))

# change tuple element: my_tuple[1]=25 # This will raise an error because tuples are immutable

type(my_tuple)


print("---------------------------------------")
print("\n")

print("Learn about set")

my_set={1,2,3,4,5 }
print(my_set)
# Add element to set
print("Add element to set")
my_set.add(6)
print(my_set)
# Remove element from set
print("Remove element from set")
my_set.remove(3)
print(my_set)

print("---------------------------------------")
print("\n")
print("Learn about Dictionary")
my_dict={"name":"Srividhya","age":25,"city":"Chennai"}
print(my_dict)
print("Accessing dictionary value using key")
print(my_dict["name"])
# Add new key-value pair to dictionary      
print("Add new key-value pair to dictionary")
my_dict["country"]="India"
print(my_dict)
# Remove key-value pair from dictionary
print("Remove key-value pair from dictionary")
del my_dict["age"]
print(my_dict)
