from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://demo:password@127.0.0.1:5432/demo')
Session = sessionmaker(bind=engine)


