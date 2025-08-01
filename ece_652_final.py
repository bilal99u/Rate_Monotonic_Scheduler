import os
import sys
import math

def main():                      # Main function to execute the scheduling algorithm
    if len(sys.argv) != 2:       # Check if the correct number of command line arguments is provided
        print("Usage: python ece_652_final.py <workload_file>") # Print usage instructions if not incorrectly run
        sys.exit(1)

    workLoadFileName = sys.argv[1]

    if not os.path.isfile(workLoadFileName):                             # Check if the workload file exists
        print(f"❌ ERROR: File '{workLoadFileName}' does not exist.")   # Print error message if file does not exist
        sys.exit(1)

    with open(workLoadFileName, 'r') as file:                             # Open the workload file for reading
        content = file.read()

    tasks = []                                                         # All taks will be stored in this list
    lines = content.strip().split('\n')                                # Split the content into lines
    schedulable = True                                                 # Flag to track if the task set is schedulable
    workloadError = False                                              # Flag to track workload errors

    """ Task creation, in this section, we parse, lines from the workload file, and create a task for each line."""
    for i, line in enumerate(lines):                            
        parts = line.strip().split(',')
        if len(parts) != 3:                 # Lines should have exactly 3 values: execution time, period, and deadline    
            print(f"Skipping line {i+1}: expected 3 values, got {len(parts)}")
            schedulable = False
            workloadError = True
            continue

        try:
            execution = float(parts[0])
            period = float(parts[1])
            deadline = float(parts[2])
        except ValueError as e:                                # converting to floats, if fail, error message
            print(f"Error parsing line {i+1}: {e}")
            schedulable = False
            workloadError = True
            continue

        task = {                                   # Create a task dictionary with execution time, period, and deadline
            'execution': execution,
            'period': period,
            'deadline': deadline
        }

        tasks.append(task)

    numberOfTasks = len(tasks)
    hyperPeriod = 1 
    for i in range(numberOfTasks):                      # Calculate the hyperperiod of the task set
        period = tasks[i]['period']
        hyperPeriod = math.lcm(int(hyperPeriod), int(period))

    jobs = []                                            # List to store all jobs generated from the tasks

    """ Job creation, in this section, we generate jobs for each task based on its period and deadline."""
    for task_id, task in enumerate(tasks):
        release_time = 0
        while release_time < hyperPeriod: # Generate jobs until the release time exceeds the hyperperiod
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
    
    preemption_counts = [0] * numberOfTasks             # List to count preemptions for each task

    for t in range(int(hyperPeriod)):                   # Iterate through each time unit in the hyperperiod
        ready_jobs = [                                  # Filter jobs that are ready to run at time t
            job for job in jobs
            if job['release_time'] <= t and
               job['remaining_time'] > 0 and
               t < job['deadline']
        ]

        if not ready_jobs:                               # If no jobs are ready, continue to the next time unit
            current_job = None
            continue

        job_to_run = min(ready_jobs, key=lambda job: job['period'])  # Select the job with the smallest period to run RMS

        if current_job is not None and current_job != job_to_run:    # If the current job is different from the job to run, and still has remaining time, means it was preempted
            if current_job['remaining_time'] > 0:
                preemption_counts[current_job['task_id']] += 1

        job_to_run['remaining_time'] -= 1
        current_job = job_to_run

    for job in jobs:                         # Check if all jobs have completed their execution, if not schedulable is False
        if job['remaining_time'] > 0:
            schedulable = False
            break

    if schedulable and not workloadError: # If the task set is schedulable and there are no workload errors
        print(1)
        print(','.join(str(p) for p in preemption_counts))
    else:
        print(0)                      # Print 0 if not shedulable
        print()

if __name__ == "__main__":
    main()
