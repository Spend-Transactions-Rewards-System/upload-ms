from dataclasses import dataclass
from src.utils.db import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import date


@dataclass
class Transaction(db.Model):
    __tablename__ = 'transaction'

    id: str
    card_id: str
    merchant: str
    mcc: int
    currency: str
    amount: float
    transaction_id: str
    transaction_date: date
    card_pan: str
    card_type: str
    reward_type: str
    reward_amount: float
    remarks: JSON

    id = db.Column(db.String(), primary_key=True)
    card_id = db.Column(db.String(), nullable=False)
    merchant = db.Column(db.String(), nullable=False)
    mcc = db.Column(db.Integer(), nullable=False)
    currency = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    transaction_id = db.Column(db.String(), nullable=False)
    transaction_date = db.Column(db.Date(), nullable=False)
    card_pan = db.Column(db.String(), nullable=False)
    card_type = db.Column(db.String(), nullable=False)
    reward_type = db.Column(db.String(), nullable=False)
    reward_amount = db.Column(db.Float(), nullable=False)

    def __init__(
            self, id, card_id, merchant, mcc, currency, amount, transaction_id, transaction_date, card_pan, card_type,
            reward_type, reward_amount
        ):
        self.id = id
        self.card_id = card_id
        self.merchant = merchant
        self.mcc = mcc
        self.currency = currency
        self.amount = amount
        self.transaction_id = transaction_id
        self.transaction_date = transaction_date
        self.card_pan = card_pan
        self.card_type = card_type
        self.reward_type = reward_type
        self.reward_amount = reward_amount

    def __repr__(self):
        return f'<Transaction ID {self.transaction_id}> <Transaction Date {self.transaction_date}> <MCC {self.mcc}> <Amonut {self.amount}> <Reward Type {self.reward_type}> <Reward Amount {self.reward_amount}>'
