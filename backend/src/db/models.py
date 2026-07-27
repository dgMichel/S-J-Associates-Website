import enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Float, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from src.db.session import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    INSPECTOR = "inspector"
    ANALYST = "analyst"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    bookings = relationship("Booking", back_populates="user")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    car_slug = Column(String(50), index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    days = Column(Integer)
    amount = Column(Float)
    currency = Column(String(3), default="usd")
    status = Column(String(20), default="pending")
    stripe_session_id = Column(String(255), nullable=True)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    customer_name = Column(String(100), nullable=True)
    customer_email = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="bookings")


class StripeAccount(Base):
    __tablename__ = "stripe_accounts"
    id = Column(Integer, primary_key=True, index=True)
    stripe_user_id = Column(String(255), unique=True)
    stripe_publishable_key = Column(String(255), nullable=True)
    access_token = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, index=True)
    brand = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    color = Column(String(30))
    plate = Column(String(20))
    price_per_day = Column(Float)
    available = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    features = Column(JSON, nullable=True)
    specs = Column(JSON, nullable=True)
    photos = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UnavailableDate(Base):
    __tablename__ = "unavailable_dates"
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    car = relationship("Car", backref="unavailable_dates")
