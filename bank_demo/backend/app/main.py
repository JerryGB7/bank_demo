# this file will control the entry point for our API

from fastapi import FastAPI

from app.routers import atms,branches, auth, service_calls

app = FastAPI(title="ATM machine tracker", description="ATM Mangement API for CashCow Project", version="0.1.0")

#include our routers in our API
app.include_router(branches.router)
app.include_router(atms.router)
app.include_router(auth.router)
app.include_router(service_calls.router)

# sample health endpoint to validate the application is running correctly 
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return{"status": "ok"}