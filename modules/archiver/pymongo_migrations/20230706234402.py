"""
Migration description here!
"""
import pymongo
from pymongo import ASCENDING 

name = '20230706234402'
dependencies = []

def upgrade(db: "pymongo.database.Database"):
    # Access your 'CongressDB' database
    cdb = db['CongressDB']

    # Access your 'CongressBill' and 'LatestAction' collections
    congress_bill = cdb['CongressBill']
    latest_action = cdb['LatestAction']

    # Create indices
    congress_bill.create_index([
        ("congress", ASCENDING), 
        ("number", ASCENDING), 
        ("originChamberCode", ASCENDING)], 
        unique=True
    )
    
    latest_action.create_index([
        ("congress", pymongo.ASCENDING), 
        ("number", ASCENDING), 
        ("originChamberCode", ASCENDING)], 
        unique=False
    )
    latest_action.create_index([("text", ASCENDING)], unique=True)


def downgrade(db: "pymongo.database.Database"):
    db['CongressDB'].drop()