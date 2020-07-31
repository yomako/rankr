import enum

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum, Integer

from ranker.db_models.base import Base


class InstTypeEnum(enum.Enum):
    Archive = 1
    Company = 2
    Education = 3
    Facility = 4
    Government = 5
    Healthcare = 6
    Nonprofit = 7
    Other = 8


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(Integer, ForeignKey("institution.id"))
    type = Column(Enum(InstTypeEnum), nullable=False, index=True)

    # Relationships
    institution = relationship("Institution", back_populates="types")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
