from fastapi import APIRouter
from db import get_session
from fastapi import Depends,APIRouter
from sqlmodel import Session,select
from schemas import Product,ProductInput,ProductOutput,CategoryInput,Category,ResponseStructure
import uvicorn

router=APIRouter(prefix='/api/products')



@router.get('/',response_model=ResponseStructure)
def get_products(productName:str|None=None,
                session:Session=Depends(get_session))->ResponseStructure:
    
    query=select(Product)
    if productName:
        query=query.where(Product.name==productName)
    
    response_data=ResponseStructure(results=session.exec(query).all(),success=True)
    return response_data



@router.post('/',response_model=ResponseStructure)
def add_products(prod:ProductInput,
                 session:Session=Depends(get_session))-> ResponseStructure:
        
        if prod:
             new_prod=Product.from_orm(prod)
             session.add(new_prod)
             session.commit()
             session.refresh(new_prod)
             session.commit()
             response_data=ResponseStructure(success=True,results=[new_prod])

             return response_data
        else:
             response_data.message="The product couldn't be added successfully"
             return response_data
             


@router.get('/{product_id}',response_model=ResponseStructure)
def get_product(product_id:int,session:Session=Depends(get_session)) -> ResponseStructure:
     
     product = session.get(Product,product_id)
     if product:
        response_data=ResponseStructure(results=[product],success=True)
        return response_data
     else:
          response_data=ResponseStructure(message=f"A product with the id of {product_id} doesn't exist")
          return response_data
     
@router.put("/{product_id}",response_model=ResponseStructure)
def edit_product(product_id:int,new_product:ProductInput,session:Session=Depends(get_session)) -> ResponseStructure:
     product=session.get(Product,product_id)
     if product:
          product.name=new_product.name
          product.quantity=new_product.quantity
          product.categoryId=new_product.categoryId
          product.price=new_product.price
          product.imgUrl=new_product.imgUrl
          session.commit()
          response_data=ResponseStructure(results=[product],success=True)
          return response_data
     else:
          response_data=ResponseStructure(message="No product with that id")
          return response_data


@router.put('/{product_id}/changeCategory',response_model=ResponseStructure)
def edit_category(category_id:int,product_id:int,session:Session=Depends(get_session)):
     targetProduct=session.get(Product,product_id)
     if targetProduct:
          targetProduct.categoryId=category_id
          session.commit()
         
          response_data=ResponseStructure(results=[targetProduct],success=True)

          return response_data
     else:
          response_data=ResponseStructure(message=f"a product with the id of {product_id} can't be found")
          return response_data


@router.post('/categories',response_model=ResponseStructure)
def add_category(new_category:CategoryInput,session:Session=Depends(get_session))->ResponseStructure:
     
     if new_category:
          new_cat = Category.from_orm(new_category)
          session.add(new_cat)
          session.commit()
          session.refresh(new_cat)
          session.commit()
          response_data = ResponseStructure(results=[new_cat],success=True)
          return response_data
     else:
          response_data=ResponseStructure(message="Couldn't add category")
          return response_data

if __name__=="__main__":
    uvicorn.run("carsharing:app",reload=True)