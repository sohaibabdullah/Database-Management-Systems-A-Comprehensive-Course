

try:
    with open('example.txt','r') as file:
        content = file.read()
        print(content)
except IOError as e:
    print(f"An error occurred: {e}")
