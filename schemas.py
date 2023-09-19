
from pydantic import BaseModel
from sqlmodel import SQLModel,Field,Relationship





class CategoryInput(SQLModel):
    name:str

class ProductInput(SQLModel):
    name:str
    price:int
    quantity:int
    imgUrl:str
    categoryId:int


class CategoryOutPut(CategoryInput):
    name:str


class Product(ProductInput,table=True):
    id:int | None=Field(primary_key=True,default=None)
    categoryId:int=Field(foreign_key='category.id')
    category:"Category"=Relationship(back_populates='products')
    



class ProductOutput(ProductInput):
    id:int
    name:str
    price:int
    quantity:int
    imgUrl:str


class Category(CategoryInput,table=True):
    id:int|None=Field(primary_key=True,default=None)
    name:str
    products:list["Product"]=Relationship(back_populates='category')
    

class CategoryOutput(CategoryInput):
    name:str
    int:int
    


class ResponseStructure(BaseModel):
    results:list
    success:bool
    message:str|None=''