from dataclasses import dataclass
from src.utils.db import db


@dataclass
class Merchant(db.Model):
    __tablename__ = 'merchant'

    id: int
    name: str
    mcc: int
    category: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    mcc = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer(), nullable=False)

    def __init__(self, id, name, mcc, category):
        self.id = id
        self.name = name
        self.mcc = mcc
        self.category = category

    def __repr__(self):
        return f'<ID: {self.id}, merchant: {self.name}, mcc: {self.mcc}, category: {self.category}>'
