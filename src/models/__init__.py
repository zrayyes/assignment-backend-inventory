from sqlalchemy import DATETIME, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Space(Base):
    __tablename__ = "storage_space"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_refrigerated = Column(Boolean)

    items = relationship("Item", back_populates="storage_space")


class ItemType(Base):
    __tablename__ = "item_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    needs_fridge = Column(Boolean)

    items = relationship("Item", back_populates="item_type")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    expiry_date = Column(DATETIME, nullable=False)
    storage_space_id = Column(Integer, ForeignKey("storage_space.id"))
    item_type_id = Column(Integer, ForeignKey("item_type.id"))

    storage_space = relationship("Space", back_populates="items")
    item_type = relationship("ItemType", back_populates="items")
