from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CongressBill(Base):
    __tablename__ = 'congress_bills'

    congress = Column(String, primary_key=True)
    number = Column(String, primary_key=True)
    origin_chamber_code = Column(String, primary_key=True)
    origin_chamber = Column(String)
    title = Column(String)
    type = Column(String)
    update_date = Column(String)
    update_date_including_text = Column(String)
    url = Column(String)

    latest_actions = relationship('LatestAction', backref='congress_bill')
    committee_reports = relationship('CommitteeReport', backref='congress_bill')
    cbo_cost_estimates = relationship('CBOCostEstimate', backref='congress_bill')
    sponsors = relationship('Sponsor', backref='congress_bill')
    laws = relationship('Law', backref='congress_bill')
    policy_areas = relationship('PolicyArea', backref='congress_bill')
    cosponsors = relationship('Cosponsor', backref='congress_bill')

class LatestAction(Base):
    __tablename__ = 'latest_actions'

    id = Column(Integer, primary_key=True)
    action_date = Column(String)
    text = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))

class CommitteeReport(Base):
    __tablename__ = 'committee_reports'

    id = Column(Integer, primary_key=True)
    citation = Column(String)
    url = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))

class CBOCostEstimate(Base):
    __tablename__ = 'cbo_cost_estimates'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    pub_date = Column(String)
    title = Column(String)
    url = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))

class Sponsor(Base):
    __tablename__ = 'sponsors'

    id = Column(Integer, primary_key=True)
    bioguide_id = Column(String)
    district = Column(String)
    first_name = Column(String)
    full_name = Column(String)
    is_by_request = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    party = Column(String)
    state = Column(String)
    url = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))

class Law(Base):
    __tablename__ = 'laws'

    id = Column(Integer, primary_key=True)
    number = Column(String)
    type = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))

class PolicyArea(Base):
    __tablename__ = 'policy_areas'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))

class Cosponsor(Base):
    __tablename__ = 'cosponsors'

    id = Column(Integer, primary_key=True)
    bioguide_id = Column(String)
    district = Column(String)
    first_name = Column(String)
    full_name = Column(String)
    is_by_request = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    party = Column(String)
    state = Column(String)
    url = Column(String)
    congress_bill_id = Column(Integer, ForeignKey('congress_bills.id'))
