import multiprocessing
import time

from fastapi import FastAPI 
 
import asyncio
import threading

app = FastAPI()

user_count = 0  # Simulated user count

def count_users_task():
    global user_count
    print(user_count)
    # In a real-world scenario, you would perform the actual user counting logic here
    user_count += 1

def periodic_task(interval: int):
    while True:
        count_users_task()

        time.sleep(interval)
    
async def periodic_hello(interval: int):
    while True:
        
        print("hello")

        await asyncio.sleep(interval)
@app.on_event("startup")
async def startup_event():
    interval = 1  # Run the task every 5 seconds
    num_processes = 2  # Number of processes to run the periodic task

    processes = []

    for _ in range(num_processes):
        process = multiprocessing.Process(target=periodic_task, args=(interval,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("All processes have finished.")

    # asyncio.create_task(periodic_task(interval))
    # asyncio.create_task(periodic_hello(interval))
@app.get("/count_users")
async def count_users():
    return {"message": "User counted in the background."}

@app.get("/get_user_count")
async def get_user_count():
    return {"user_count": user_count}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000 )
