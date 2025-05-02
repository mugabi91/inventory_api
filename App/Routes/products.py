from fastapi import APIRouter, status, HTTPException, Depends
from App import Models
from ..Schemas import products
from App.Database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import update
from rich import print
from typing import List

products_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# get all products 👍
@products_router.get("/",status_code=status.HTTP_200_OK, response_model=List[products.ProductResponseSchema])
async def get_products(db:Session = Depends(get_db)):
    all_products = db.query(Models.Products).all()
    return all_products

# get a particular product by product_id 👍
@products_router.get("/{product_id}",status_code=status.HTTP_200_OK)
async def get_product(product_id:int,db:Session = Depends(get_db)):
    
    # check product exists
    product = db.query(Models.Products).filter(Models.Products.Product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} doesnt Exist")
    return product

# create Product  👍
@products_router.post("/",status_code=status.HTTP_201_CREATED)
async def create_product(product_data:products.ProductsIn, db:Session = Depends(get_db)):
    # product = check_product_exists(product_data.id)
    # if not product:
    new_product = Models.Products(**product_data.model_dump())
    db.add(new_product)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# update Product 👍
@products_router.put("/{product_id}", status_code=status.HTTP_201_CREATED)
async def updateproduct(product_id: int, product_data: products.ProductsIn, db: Session = Depends(get_db)):
    
    # Retrieve the product from the database
    product = db.query(Models.Products).filter(Models.Products.Product_id == product_id).first()

    # If product does not exist, raise an error
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} doesn't exist")

    # Update the product with new data
    stmt = (
        update(Models.Products)
        .where(Models.Products.Product_id == product_id)
        .values(**product_data.model_dump())
    )
    db.execute(stmt)
    db.commit()
    
    updated_product = db.query(Models.Products).filter(Models.Products.Product_id == product_id).first()
    
    return updated_product



# Delete a particular product with product_id 👍
@products_router.delete("/{product_id}",status_code=status.HTTP_200_OK)
async def delete_product(product_id:int, db: Session = Depends(get_db)):
    
    # Retrieve the product from the database
    product = db.query(Models.Products).filter(Models.Products.Product_id == product_id).first()
    # If product does not exist, raise an error
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product_id} doesn't exist")
    
    db.query(Models.Products).filter(Models.Products.Product_id == product_id).delete()
    db.commit()
