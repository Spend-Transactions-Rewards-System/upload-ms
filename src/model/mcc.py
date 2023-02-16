from dataclasses import dataclass
from src.utils.db import db


@dataclass
class MCC(db.Model):
    __tablename__ = 'mcc'

    mcc: int
    description: str

    mcc = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __init__(self, mcc, description):
        self.mcc = mcc
        self.description = description

    def __repr__(self):
        return f'<MCC: {self.mcc}, description: {self.description}>'
