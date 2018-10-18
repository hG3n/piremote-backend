#!/usr/bin/env python3
from database.base import TableBase
import database.constants
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class RFReceiver(TableBase):
    """
        Describes a 433Mhz receiver
    """
    __tablename__ = 'rf-receiver'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    alias = Column(String(50))
    on_signal_id = Column(Integer, ForeignKey('rf-signal.id'))
    off_signal_id = Column(Integer, ForeignKey('rf-signal.id'))
    state = Column(Boolean, nullable=False, default=False)
