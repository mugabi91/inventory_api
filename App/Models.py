from fastapi import FastAPI
from sqlalchemy import (TIMESTAMP, String, 
                        Column,Integer,
                        func,ForeignKey
                        )

from sqlalchemy.orm import  relationship
from sqlalchemy import String, Column, func, Float, Integer, ForeignKey ,DateTime,Numeric
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.declarative import declarative_base

# Base model
Base = declarative_base()


# Products Table
class Products(Base):
    __tablename__ = "Products"
    
    Product_id = Column(Integer, primary_key=True, nullable=False)
    Product_name = Column(String, nullable=False)
    Product_price = Column(Numeric, nullable=True)
    Product_stock = Column(Numeric, nullable=True)
    Product_description = Column(String, nullable=True)
    
    # Relationship: one product to many sales
    sales = relationship("Sales", back_populates="product")

# Users Table
class Users(Base):
    __tablename__ = "Users"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    userEmail = Column(String(255), nullable=False, unique=True)
    userFullName = Column(String(100), nullable=False)
    user_pwd = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship: one user to many sales
    sales = relationship("Sales", back_populates="user")

# Sales Table
class Sales(Base):
    __tablename__ = "Sales"
    
    transaction_id = Column(Integer, primary_key=True, nullable=False)
    transaction_date_time = Column(DateTime, server_default=func.now())
    quantity = Column(Integer, nullable=False)
    
    Product_id = Column(Integer, ForeignKey("Products.Product_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    
    # ORM relationships
    product = relationship("Products", back_populates="sales")
    user = relationship("Users", back_populates="sales")


# Sales Table
# class Reports(Base):
#     pass