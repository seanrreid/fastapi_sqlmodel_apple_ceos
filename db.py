from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = 'postgresql://postgres@localhost/apple_ceos'
DATABASE_URL = 'postgresql://postgres.swepwqrdkebfdvzcaezn:DJ7$if9w6jd2@aws-0-us-west-1.pooler.supabase.com:6543/postgres'

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
