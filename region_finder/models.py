from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship)


class Base(DeclarativeBase):
    pass


class Region(Base):
    """Модель региона РФ."""

    __tablename__ = 'regions'

    region_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    aliases: Mapped[List["Alias"]] = relationship(back_populates='region')

    def __repr__(self) -> str:
        return f'<Region {self.name}>'


class Alias(Base):
    """Модель признаков региона РФ."""

    __tablename__ = 'aliases'

    alias_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey('regions.region_id'), nullable=False)
    region: Mapped["Region"] = relationship(back_populates='aliases')

    def __repr__(self) -> str:
        return f'<Alias {self.name}>'


class Address(Base):
    """Почтовый адрес РФ."""

    __tablename__ = 'addresses'

    postcode: Mapped[str] = mapped_column(primary_key=True, index=True)
    area: Mapped[str] = mapped_column(nullable=True)
    locality: Mapped[str] = mapped_column(nullable=True)
    region_id: Mapped[int] = mapped_column(
        ForeignKey('regions.region_id'),
        nullable=False
    )

    def __repr__(self) -> str:
        return f'<Address {self.postcode} - {self.area}>'
