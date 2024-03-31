from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class VariantBase(BaseModel):
    size: str
    color: str
    material: str

class ProductBase(BaseModel):
    product_name: str

class Pro(BaseModel):
    product_id: int

class Product(ProductBase):
    variants: List[VariantBase]

class Variant(BaseModel):
    product_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#------------------------

@app.post("/Add_Product_Name/")
async def add_product(product: ProductBase, db:db_dependency):
    db_product = models.Products(pduct_name = product.product_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {"Message": "Product Name added successfully."}

#------------------------

@app.post("/Add_Product_and_Variants/")
async def add_product_and_variants(product: Product, db:db_dependency):
    db_product = models.Products(pduct_name = product.product_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    for variant in product.variants:
        db_variant = models.Variants(size= variant.size, color= variant.color, material= variant.material, product_id= db_product.pduct_id, product_name= db_product.pduct_name)
        db.add(db_variant)
    db.commit()

    return {"Message": "Product and Variants added successfully."}

#------------------------

@app.post("/Add_Variants_for_Existing_Product/{product_name}/")
async def add_variants(product_name: str, variants: List[VariantBase], db:db_dependency):
    db_product = db.query(models.Products).filter(models.Products.pduct_name == product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Message: Product not found.")
    for variant in variants:
        db_variant = models.Variants(size= variant.size, color= variant.color, material= variant.material, product_id= db_product.pduct_id, product_name= db_product.pduct_name)
        db.add(db_variant)
    db.commit()

    return {"Message": "Variants added successfully."}

#------------------------

@app.get("/Get_Full_Data/{product_name}")
async def get_product(product_name: str, db:db_dependency):
    db_product = db.query(models.Products).filter(models.Products.pduct_name == product_name).first()
    db_variant = db.query(models.Variants).filter(models.Variants.product_name == product_name).all()
    l = []
    for i in range(len(db_variant)):
        d = {"Size": db_variant[i].size, "Color": db_variant[i].color, "Material": db_variant[i].material }
        l.append(d)

    if not db_product:
        raise HTTPException(status_code=404, detail="Message: Product not found.")
    
    if l == []:
        result = {"Product- ": db_product.pduct_name, "Variants- ": "No variants are added to the database."}
    else:
        result = {"Product- ": db_product.pduct_name, "Variants- ": l }

    return result

#------------------------

@app.put("/Update_Product_Data/{product_id}")
async def update_product(product_id: int, product_update: ProductBase, variant_update: Variant, db:db_dependency):
    db_product = db.query(models.Products).filter(models.Products.pduct_id == product_id).first()
    db_var = db.query(models.Variants).filter(models.Variants.product_id == product_id).all()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Message: Product not found.")
    
    db_product.pduct_name = variant_update.product_name if product_update.product_name is not None else db_product.pduct_name
    a = len(db_var)
    while(a>=0):
        try: 
            db_variant = db.query(models.Variants).filter(models.Variants.product_id == product_id).first()
            db_variant.product_name = product_update.product_name if product_update.product_name is not None else db_product.pduct_name
            db.add(db_variant)
            a = a-1
            db.commit()
            result = {"Message": "Product data was updated successfully."}
        except:
            return {"Message": "No variant data found, add variants."}
        
    #return result
    return result

#------------------------

@app.put("/Update_Variant_Data/{variant_id}")
async def update_variant(variant_id: int, variant_update: VariantBase, db:db_dependency):
    db_variant = db.query(models.Variants).filter(models.Variants.var_id == variant_id).first()
    
    if not db_variant:
        raise HTTPException(status_code=404, detail="Message: Variant not found.")
    
    db_variant.size = variant_update.size if variant_update.size is not None else db_variant.size
    db_variant.color = variant_update.color if variant_update.color is not None else db_variant.color
    db_variant.material = variant_update.material if variant_update.material is not None else db_variant.material
    db.commit()
        
    return {"Message": "Variant data was updated successfully."}

#------------------------

@app.delete("/Delete_Variant/{variant_id}")
async def delete_variant(variant_id: int, db:db_dependency):
    db_variant = db.query(models.Variants).filter(models.Variants.var_id == variant_id).first()

    if not db_variant:
        raise HTTPException(status_code=404, detail="Message: Variant not found.")
    
    db.delete(db_variant)  # Delete the retrieved Variant object
    db.commit()  # Commit the deletion to the database
    result = {"Product- ": db_variant.product_name, "Variant- ": {"Size": db_variant.size, "Colour" :db_variant.color, "Material": db_variant.material},  
              "Message": "Variant deleted successfully."}

    return result

#------------------------

@app.delete("/Delete_all_Variants/{product_name}")
async def delete_all_variants(product_name: str, db:db_dependency):
    db_product = db.query(models.Products).filter(models.Products.pduct_name == product_name).first()
    if not db_product:
            raise HTTPException(status_code=404, detail="Message: Product not found.")
    
    db_variant = db.query(models.Variants).filter(models.Variants.product_name == product_name).all()
    l = []
    for i in range(len(db_variant)):
        d = {"Size": db_variant[i].size, "Color": db_variant[i].color, "Material": db_variant[i].material }
        l.append(d)

    if l == []:
        result = {"Product- ": db_product.pduct_name, "Message": "No variants are added to the database."}
    else:
        result = {"Product- ": db_product.pduct_name, "Variants- ": l, "Message": "All variants deleted successfully."}

    if db_variant:
        for variant in db_variant:
            db.delete(variant)  # Delete each Variant object from the list
        db.commit() # Commit the deletion to the database

    return result

#------------------------

@app.delete("/Delete_Product/{product_name}")
async def delete_product(product_name: str, db:db_dependency):
    db_product = db.query(models.Products).filter(models.Products.pduct_name == product_name).first()

    if not db_product:
            raise HTTPException(status_code=404, detail="Message: Product not found.")
    
    db_variant = db.query(models.Variants).filter(models.Variants.product_name == product_name).all()
    
    if db_variant:
        return {"Message" : "Cannot delete due to linked data. First go to delete variants and then repeat."}
    else:
        db_product = db.query(models.Products).filter(models.Products.pduct_name == product_name).first()
        db.delete(db_product)  # Delete the retrieved Item object
        db.commit()  # Commit the deletion to the database
        result = {"Product- ": db_product.pduct_name, "Message": "Product deleted successfully."}

    return result

#------------------------
