from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class Products(Base):
    __tablename__ = 'products'
    pduct_id = Column(Integer, primary_key=True, index=True)
    pduct_name = Column(String, index=True)

class Variants(Base):
    __tablename__ = 'variants'
    var_id = Column(Integer, primary_key= True, index=True)
    size = Column(String, index=True)
    color = Column(String, index=True)
    material = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.pduct_id")) 
    product_name = Column(String, index=True)