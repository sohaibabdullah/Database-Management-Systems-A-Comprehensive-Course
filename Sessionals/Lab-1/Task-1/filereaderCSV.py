
#Method 1:
print("Method 1:")
try:
    with open('data.csv','r') as file:
        content = file.read()
        print(content)
except IOError as e:
    print(f"An error occurred: {e}")


#Method 2:
print("Method 2:")

import csv

try:
    with open('data.csv','r',newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
except IOError as e:
    print(f"An error occurred {e}")