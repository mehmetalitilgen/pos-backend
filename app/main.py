from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def sshutdown_event():
    print

# app.include_router(v1_router)



