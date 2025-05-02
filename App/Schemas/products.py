from pydantic import BaseModel
from typing import Optional

class ProductsIn(BaseModel):
    Product_name:str
    Product_price:float
    Product_stock:int=0
    Product_description:  Optional[str] = None
    

class ProductResponseSchema(BaseModel):
    Product_id: int
    Product_name: str
    Product_price: float
    Product_stock: int
    Product_description: Optional[str] = None 
