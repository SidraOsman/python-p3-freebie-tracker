from sqlalchemy import ForeignKey, Column, Integer, String, MetaData , Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


company_dev = Table(
    'company_dev',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'),primary_key=True),
    extend_existing=True
)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    devs = relationship('Dev', secondary=company_dev, back_populates='companies')
    freebies = relationship('Freebie' , backref=backref('company'))

    def get_freebies(self,session):
        return session.query(Freebie).filter(Freebie.company_id_id == self.id).all() 
    
    def __repr__(self):
        return f'<Company {self.name}>'
     

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())


    companies = relationship('Company' , secondary=company_dev, back_populates="devs")
    freebies = relationship('Freebie' , backref=backref('dev'))

        
    def get_dev_freebies(self,session):
        return (session.query(Freebie) .filter(Freebie.dev_id == self.id).all())
    
        
    def get_dev_companies(self,session): 
        return (
            session.query(Company)
            .join(company_dev)
            .filter(company_dev.c.dev_id == self.id)
            .all()
        )

    def __repr__(self):
        return f'<Dev {self.name}>'
    

    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer() , primary_key=True)
    item_name = Column(String())
    value = Column(Integer())


    company_id= Column(Integer, ForeignKey('companies.id'))
    dev_id = Column(Integer , ForeignKey('devs.id'))


    def get_freebie_for_dev(self,session): 
        return session.query(Dev).filter(Dev.id == self.dev_id).first()
    
    def get_freebie_for_company(self,session):
        return session.query(Company).filter(Company.id == self.company_id).first()
    
    def freebie_order(self,session): 
        return (f"Freebie for  {self.get_freebie_for_company(session).name} by {self.get_freebie_for_dev(session).name}: Item_name:{self.item_name} value:{self.value}")
    

    def __repr__(self):
        return f'<Freebie {self.item_name}>'




