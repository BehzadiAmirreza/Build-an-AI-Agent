from functions.run_python_file import run_python_file

if __name__ == "__main__":
    # 1. Run main.py with no arguments
    result = run_python_file("calculator", "main.py")
    print('run_python_file("calculator", "main.py"):')
    print(result)
    print()

    # 2. Run main.py with argument "3 + 5"
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print(result)
    print()

    # 3. Run tests.py (should execute the test file)
    result = run_python_file("calculator", "tests.py")
    print('run_python_file("calculator", "tests.py"):')
    print(result)
    print()

    # 4. Attempt to run a file outside working directory
    result = run_python_file("calculator", "../main.py")
    print('run_python_file("calculator", "../main.py"):')
    print(result)
    print()

    # 5. Attempt to run a nonexistent file
    result = run_python_file("calculator", "nonexistent.py")
    print('run_python_file("calculator", "nonexistent.py"):')
    print(result)
    print()
