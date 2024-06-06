from db.base_class import Base  # noqa
from sqlalchemy import BigInteger, Boolean, Column, Integer, String  # noqa


class Member(Base):
    id = Column(Integer, primary_key=True, index=True)
    ext_id = Column(BigInteger, index=True)
    name = Column(String, index=True)
    country = Column(String)
    city = Column(String)
    position = Column(String, index=True)
    company = Column(String, index=True)
    company_country = Column(String)
    company_description = Column(String)
    company_website = Column(String)
    hobby = Column(String)
