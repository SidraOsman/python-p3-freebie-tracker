#!/usr/bin/env python3

# Script goes here!


import random
from faker import Faker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base , Company, Freebie, Dev

print ("Seeding starts!!")
if __name__ == '__main__': 

    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

        
    companies= []
    for _ in range (20):
        company = Company(
            name = fake.unique.name(),
            founding_year = fake.year()
        )
        session.add(company)
        session.commit()
        companies.append(company)

    devs = []
    for _ in range (20):
        dev = Dev(
            name = fake.unique.name()
        )
        session.add(dev)
        session.commit()
        devs.append(dev)

    freebies = []
    for company in companies:
        for i in range(random.randint(1,5)):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()

            freebie = Freebie(
                item_name = fake.unique.name(),
                value = random.randint(500,1500),
                company_id = company.id,
                dev_id = dev.id
            )
            freebies.append(freebie)

    session.bulk_save_objects(freebies)
    session.commit()
    session.close()


