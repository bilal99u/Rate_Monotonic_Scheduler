import os

print("Welcome to Ahmad Bilal Irfan's RMS Simulator")

workLoadFileName = "" # Initialize the workload file name
content = "" # Initialize content variable, which will hold the file content

# This loop will continue to read the workload until a valid file is provided 
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
            
    else:
        print(f"File '{workLoadFileName}' does not exist, Please enter a valid file name.")

print ("File was read successfully.")

tasks = []

# Splitting content into individual lines
lines = content.strip().split('\n')


# Step 2: Parse each line
for i, line in enumerate(lines):
    parts = line.strip().split(',')

    if len(parts) != 3:
        print(f"Skipping line {i+1}: expected 3 values, got {len(parts)}")
        continue

    try:
        execution = float(parts[0])
        period = float(parts[1])
        deadline = float(parts[2])
    except ValueError as e:
        print(f"Error parsing line {i+1}: {e}")
        continue

    task = {
        'execution': execution,
        'period': period,
        'deadline': deadline
    }

    tasks.append(task)
print (tasks)