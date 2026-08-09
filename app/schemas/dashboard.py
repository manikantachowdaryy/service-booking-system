from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    total_users: int
    total_providers: int
    total_customers: int
    total_services: int
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_revenue: float


class ProviderDashboardResponse(BaseModel):
    total_services: int
    total_bookings: int
    pending_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_revenue: float
    average_rating: float


class CustomerDashboardResponse(BaseModel):
    upcoming_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_spent: float