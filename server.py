from fastapi import FastAPI, Query, HTTPException
from .client.rq_client import queue
from .queues.worker import process_query


# creating an app
app = FastAPI()

# creating a sample route
@app.get('/')
def root():
    return {"status": 'Server is up and running'}


# creating chat route
@app.post('/chat') # creating a post route
def chat(
        query: str = Query(..., description="The chat query of user")
):
    job = queue.enqueue(process_query, query)

    return {"status": "queued", "job_id": job.id}


# creating another route
@app.get('/job-status') 
def get_result(
        job_id: str = Query(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    # result = job.return_value()

    # return {"result": result}
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found or expired")

    status = job.get_status()

    return {
        "job_id": job.id,
        "status": status,
        "result": job.return_value() if status == "finished" else None
    }