from fastapi import APIRouter, status, HTTPException, Depends
from App import Models
from ..Schemas import users
from App.Database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import List
from ..utils import  hash_pwd

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# get all Users 👍
@users_router.get("/",status_code=status.HTTP_200_OK, response_model=List[users.UsersResponseSchema])
async def get_users(db:Session = Depends(get_db)):
    all_users = db.query(Models.Users).all()
    return all_users

# get a particular Users by user_name/UserEmail 👍
@users_router.get("/email/{user_name}",status_code=status.HTTP_200_OK, response_model=users.UsersResponseSchema)
async def get_user(user_name:str,db:Session = Depends(get_db)):
    # check User exists
    user = db.query(Models.Users).filter(Models.Users.userEmail == user_name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with UserName {user_name} doesnt Exist")
    return user

# create User  👍
@users_router.post("/",status_code=status.HTTP_201_CREATED, response_model=users.UsersResponseSchema)
async def create_user(user_data:users.UsersIn, db:Session = Depends(get_db)):
    user = db.query(Models.Users).filter(Models.Users.userEmail == user_data.userEmail).first()
    if not user:
        user_data.user_pwd = hash_pwd(user_data.user_pwd)
        new_user = Models.Users(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status.HTTP_409_CONFLICT, f"User with UserName {user_data.userEmail} already Exists")

# update User 👍
@users_router.put("/email/{user_name}", status_code=status.HTTP_201_CREATED, response_model=users.UsersResponseSchema)
async def updateUser(user_name: str, user_data: users.UsersIn, db: Session = Depends(get_db)):
    # Retrieve the User from the database
    user = db.query(Models.Users).filter(Models.Users.userEmail == user_name).first()
    # If User does not exist, raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with UserName {user_name} doesn't exist")
    user_data.user_pwd = hash_pwd(user_data.user_pwd)
    # Update the User with new data
    stmt = (
        update(Models.Users)
        .where(Models.Users.userEmail == user_name)
        .values(**user_data.model_dump())
    )
    db.execute(stmt)
    db.commit()
    
    updated_user = db.query(Models.Users).filter(Models.Users.userEmail == user_name).first()
    
    return updated_user


# Delete a particular User with user_name /Email_id 👍
@users_router.delete("/email/{user_name}",status_code=status.HTTP_200_OK)
async def delete_user(user_name:str, db: Session = Depends(get_db)):

    # Retrieve the user_name from the database
    user = db.query(Models.Users).filter(Models.Users.userEmail == user_name).first()
    # If user_name does not exist, raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with UserName {user_name} doesn't exist")
    
    db.query(Models.Users).filter(Models.Users.userEmail == user_name).delete()
    db.commit()
