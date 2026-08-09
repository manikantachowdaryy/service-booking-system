from fastapi import FastAPI

from app.routers import (
    auth,
    service,
    availability,
    booking,
    payment,
    review,
    notification,
    dashboard,
)

app = FastAPI(
    title="Service Booking & Appointment Management System",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(service.router)
app.include_router(availability.router)
app.include_router(booking.router)
app.include_router(payment.router)
app.include_router(review.router)
app.include_router(notification.router)
app.include_router(dashboard.router)


@app.get("/")
def home():
    return {
        "message": "Service Booking API is Running 🚀"
    }