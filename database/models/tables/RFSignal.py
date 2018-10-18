#!/usr/bin/env python3
from database.base import TableBase
import database.constants
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class RFSignal(TableBase):
    """
        Describes a 433Mhz signal
    """
    __tablename__ = 'rf-signal'
    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False)
    pulselength = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False)

