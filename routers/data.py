from fastapi import APIRouter
from db import get_session
from fastapi import HTTPException,Depends,APIRouter
from sqlmodel import Session,select
from schemas import Product,ProductInput,ProductOutput,CategoryInput,Category,ResponseStructure
import uvicorn

router=APIRouter(prefix='/api/products')


# The success boolean will change based on the status of each request
response_structure={
     "success":True,
     "results":[]
}

@router.get('/',response_model=ResponseStructure)
def get_products(productName:str|None=None,
                session:Session=Depends(get_session))->list[Product]:
    
    query=select(Product)
    if productName:
        query=query.where(Product.name==productName)
    
    response_data=ResponseStructure(results=session.exec(query).all(),success=True)
    return response_data



@router.post('/',response_model=ResponseStructure)
def add_products(prod:ProductInput,
                 session:Session=Depends(get_session))-> Product:
        
        if prod:
             new_prod=Product.from_orm(prod)
             session.add(new_prod)
             session.commit()
             session.refresh(new_prod)
             session.commit()
             response_data=ResponseStructure(success=True,results=prod)

             return response_data
        else:
             response_data.message="The product couldn't be added successfully"
             return response_data
             


@router.get('/{product_id}',response_model=Product)
def get_product(product_id:int,session:Session=Depends(get_session)):
     product = session.get(Product,product_id)
     if product:
        return product
     else:
          raise HTTPException(status_code=404,detail=f"A product with the id of {product_id} doesn't exist")
     

@router.put('/{product_id}/changeCategory',response_model=Product)
def edit_category(category_id:int,product_id:int,session:Session=Depends(get_session)):
     targetProduct=session.get(Product,product_id)
     if targetProduct:
          targetProduct.categoryId=category_id
          session.commit()
          return targetProduct
     else:
          return HTTPException(status_code=402,detail=f"A product with the id of {product_id} hasn't been found")
     


@router.post('/categories',response_model=Category)
def add_category(new_category:CategoryInput,session:Session=Depends(get_session))->Category:
     
     new_cat = Category.from_orm(new_category)
     if new_cat:
          session.add(new_cat)
          session.commit()
          session.refresh(new_cat)
          session.commit()
          return new_cat


if __name__=="__main__":
    uvicorn.run("carsharing:app",reload=True)