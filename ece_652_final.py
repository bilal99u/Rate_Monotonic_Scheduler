import os
import sys
import math

def main():
    if len(sys.argv) != 2:
        print("Usage: python ece_652_final.py <workload_file>")
        sys.exit(1)

    workLoadFileName = sys.argv[1]

    if not os.path.isfile(workLoadFileName):
        print(f"❌ ERROR: File '{workLoadFileName}' does not exist.")
        sys.exit(1)

    with open(workLoadFileName, 'r') as file:
        content = file.read()

    tasks = []
    lines = content.strip().split('\n')
    schedulable = True
    workloadError = False # Flag to track workload errors
    for i, line in enumerate(lines):
        parts = line.strip().split(',')

        if len(parts) != 3:
            print(f"Skipping line {i+1}: expected 3 values, got {len(parts)}")
            schedulable = False
            workloadError = True
            continue

        try:
            execution = float(parts[0])
            period = float(parts[1])
            deadline = float(parts[2])
        except ValueError as e:
            print(f"Error parsing line {i+1}: {e}")
            schedulable = False
            workloadError = True
            continue

        task = {
            'execution': execution,
            'period': period,
            'deadline': deadline
        }

        tasks.append(task)

    numberOfTasks = len(tasks)
    hyperPeriod = 1 
    for i in range(numberOfTasks):
        period = tasks[i]['period']
        hyperPeriod = math.lcm(int(hyperPeriod), int(period))

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
    
    preemption_counts = [0] * numberOfTasks

    for t in range(int(hyperPeriod)):
        ready_jobs = [
            job for job in jobs
            if job['release_time'] <= t and
               job['remaining_time'] > 0 and
               t < job['deadline']
        ]

        if not ready_jobs:
            current_job = None
            continue

        job_to_run = min(ready_jobs, key=lambda job: job['period'])

        if current_job is not None and current_job != job_to_run:
            if current_job['remaining_time'] > 0:
                preemption_counts[current_job['task_id']] += 1

        job_to_run['remaining_time'] -= 1
        current_job = job_to_run

    for job in jobs:
        if job['remaining_time'] > 0:
            schedulable = False
            break

    if schedulable and not workloadError:
        print(1)
        print(','.join(str(p) for p in preemption_counts))
    else:
        print(0)
        print()

if __name__ == "__main__":
    main()
