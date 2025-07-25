import os
import math
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

# Number of tasks and details of each task
numberOfTasks = len(tasks)
hyperPeriod = 1 
for i in range(numberOfTasks):
    period = tasks[i]['period']
    hyperPeriod = math.lcm(int(hyperPeriod), int(period))
    print(f"Task {i+1}: Execution: {tasks[i]['execution']}, Period: {tasks[i]['period']}, Deadline: {tasks[i]['deadline']}")

print(f"Total number of tasks: {numberOfTasks}")
print(f"Hyperperiod after Task {numberOfTasks}: {hyperPeriod}")
# Generating jobs for one hyperperiod
jobs = []

for task_id, task in enumerate(tasks):
    release_time = 0
    while release_time < hyperPeriod:
        job = {
            'task_id': task_id,
            'release_time': release_time,
            'deadline': release_time + task['deadline'],
            'remaining_time': task['execution'],
            'period': task['period']  
        }
        jobs.append(job)
        release_time += task['period']

print (jobs)
print ('test commit to github')