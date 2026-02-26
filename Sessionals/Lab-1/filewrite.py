try:
    with open('example.txt','w') as file:
        file.write("Hello, Assalamualikum...")
except IOError as e:
    print(f"An error occurred: {e}")
