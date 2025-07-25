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

current_job = None
schedulable = True
preemption_counts = [0] * numberOfTasks


for t in range(int(hyperPeriod)):
    # Find ready jobs
    ready_jobs = [
        job for job in jobs
        if job['release_time'] <= t and
           job['remaining_time'] > 0 and
           t < job['deadline']
    ]

    if not ready_jobs:
        current_job = None  # CPU idle
        continue

    # Pick job with highest priority (lowest period)
    job_to_run = min(ready_jobs, key=lambda job: job['period'])

    # Preemption check: only if there was a previously running job
    if current_job is not None and current_job != job_to_run:
        if current_job['remaining_time'] > 0:
            preemption_counts[current_job['task_id']] += 1

    # Run job
    job_to_run['remaining_time'] -= 1
    print(f"Time {t}: Running Task {job_to_run['task_id'] + 1}, Remaining Time: {job_to_run['remaining_time']}")

    # Update current_job pointer
    current_job = job_to_run


for job in jobs:
    if job['remaining_time'] > 0:
        schedulable = False
        break

if schedulable:
    print(1)
    print(','.join(str(p) for p in preemption_counts))
else:
    print(0)
    print()
print ("Printed number of tasks:", numberOfTasks)
print("Hyperperiod:", hyperPeriod)  
print("Preemption counts:", ','.join(str(p) for p in preemption_counts))
print("Tasks:")