import os

print("Welcome to Ahmad Bilal Irfan's RMS Simulator")

workLoadFileName = "" # Initialize the workload file name
content = "" # Initialize content variable, which will hold the file content

while (True):
    workLoadFileName = input("Enter the workload file name: ")
    print("You entered: " + workLoadFileName)

    # Check if the file exists
    if os.path.isfile(workLoadFileName):
        print(f"File '{workLoadFileName}' exists. Opening in read mode...")
        with open(workLoadFileName, 'r') as file:
            content = file.read()
            print("File content:")
            print(content)
            break
            # You can add parsing logic here
    else:
        print(f"File '{workLoadFileName}' does not exist, Please enter a valid file name.")

print ("File was read successfully.")