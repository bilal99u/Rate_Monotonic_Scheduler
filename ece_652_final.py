import os

print("Welcome to Ahmad Bilal Irfan's RMS Simulator")

workLoadFileName = input("Enter the workload file name: ")
print("You entered: " + workLoadFileName)
print(type(workLoadFileName))

# Check if the file exists
if os.path.isfile(workLoadFileName):
    print(f"File '{workLoadFileName}' exists. Opening in read mode...")
    with open(workLoadFileName, 'r') as file:
        content = file.read()
        print("File content:")
        print(content)
        # You can add parsing logic here
else:
    print(f"File '{workLoadFileName}' does not exist.")