from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
def get_files_info_test():
    print(f"Result for current directory: {get_files_info("calculator", ".")}")
    print(f"Result for 'pkg' directory: {get_files_info("calculator", "pkg")}")
    print(f"Result for '/bin' directory: {get_files_info("calculator", "/bin")}")
    print(f"Result for '../' directory: {get_files_info("calculator", "../")}")

def get_file_content_test():
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

def write_file_test():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "test/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

def run_python_test():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))


run_python_test()
