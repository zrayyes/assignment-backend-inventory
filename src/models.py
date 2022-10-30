from sqlalchemy import DATE, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from src.helpers import format_date_to_str

Base = declarative_base()


class Space(Base):
    __tablename__ = "storage_space"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_refrigerated = Column(Boolean)

    items = relationship("Item", back_populates="storage_space")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "is_refrigerated": self.is_refrigerated,
        }


class ItemType(Base):
    __tablename__ = "item_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    needs_fridge = Column(Boolean)

    items = relationship("Item", back_populates="item_type")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "needs_fridge": self.needs_fridge,
        }


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    expiry_date = Column(DATE, nullable=False)
    storage_space_id = Column(Integer, ForeignKey("storage_space.id"), nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_type.id"), nullable=False)

    storage_space = relationship("Space", back_populates="items")
    item_type = relationship("ItemType", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.item_type.name,
            "storage_space": self.storage_space.name,
            "expiry_date": format_date_to_str(self.expiry_date),
            "needs_fridge": self.item_type.needs_fridge,
        }

    def __lt__(self, other):
        return self.expiry_date < other.expiry_date
