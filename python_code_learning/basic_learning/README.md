# Python Basic Learning

## Overview

This folder contains a collection of Python programs and notebooks created while learning the **fundamentals of Python programming**. The examples demonstrate essential concepts such as **basic syntax, functions, modules, file handling, and simple application development**.

The goal of this module is to build a **strong foundation in Python**, which is essential before progressing to advanced areas such as **web development, data engineering, and AI/Generative AI applications**.

---

## Repository Structure

```text
python_code_learning/basic_learning/
│
├── calculator_app.py
├── file_handling.ipynb
├── package_testing.py
├── python_functions.py
├── python_learning.py
└── README.md
```

Each file in this directory focuses on a specific Python concept to help reinforce practical learning.

---

## File Descriptions

### 1. calculator_app.py

This script implements a **simple command-line calculator application**.
It allows users to perform common arithmetic operations by entering numbers and selecting an operation.

**Key Concepts Covered**

* Function creation
* Conditional logic
* User input handling
* Basic arithmetic operations

**Example Concept**

```python
def add(a, b):
    return a + b
```

This program demonstrates how functions can be used to organize logic and build a simple interactive application.

---

### 2. file_handling.ipynb

This Jupyter Notebook demonstrates **file handling techniques in Python**, showing how Python programs can interact with files stored on the system.

**Key Concepts Covered**

* Opening files
* Reading file content
* Writing data to files
* Appending new content
* Using `with` statements for safe file operations

**Example**

```python
with open("sample.txt", "r") as file:
    data = file.read()
    print(data)
```

File handling is an essential skill for tasks such as **data processing, logging, and configuration management**.

---

### 3. package_testing.py

This script demonstrates how to **import and use Python modules or packages**.
It helps illustrate how Python projects can be structured using reusable components.

**Key Concepts Covered**

* Importing built-in or external modules
* Using functions from imported packages
* Understanding modular programming

**Example**

```python
import math

print(math.sqrt(16))
```

This concept is fundamental when working with **Python libraries and larger applications**.

---

### 4. python_functions.py

This file focuses on the **definition and usage of functions in Python**.

Functions allow developers to write modular and reusable code, improving maintainability and readability.

**Key Concepts Covered**

* Function definition
* Parameters and arguments
* Returning values
* Code modularization

**Example**

```python
def greet(name):
    print("Hello", name)

greet("Python")
```

---

### 5. python_learning.py

This script contains examples of **basic Python programming constructs** used during the learning process.

**Key Concepts Covered**

* Variables and data types
* Arithmetic operations
* Conditional statements
* Loops
* Basic program structure

Example:

```python
a = 10
b = 5

print("Addition:", a + b)
```

This file serves as a **general practice environment for understanding Python syntax and logic building**.

---

## How to Run the Programs

### Run Python Scripts

Navigate to the project directory:

```bash
cd python_code_learning/basic_learning
```

Run a Python script:

```bash
python calculator_app.py
```

or

```bash
python python_functions.py
```

---

### Run the Jupyter Notebook

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open and execute:

```text
file_handling.ipynb
```

---

## Key Concepts Practiced

This module focuses on the following Python fundamentals:

* Python syntax and program structure
* Functions and modular programming
* Arithmetic and logical operations
* File handling in Python
* Module and package usage
* Building simple command-line applications

---

## Learning Outcomes

After working through the examples in this folder, you will be able to:

* Understand the core syntax and structure of Python programs
* Write reusable functions to organize code
* Work with files for reading and writing data
* Use Python modules and packages effectively
* Develop simple command-line applications

These foundational skills prepare learners for **advanced Python topics such as web frameworks, data processing, and AI development**.

---

## Author

**Srividhya Ganesan**

This folder is part of the **GenAI Learning Repository**, which documents hands-on exploration of **Python programming, AI frameworks, and Generative AI development**.
