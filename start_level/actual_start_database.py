from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# creating the file sqlite_start_base in my flder, so I can go ahead and create the engine
SQL_ALCHEMY_START_DB = "sqlite:///sqlite_start_base.db"
engine = create_engine(
    SQL_ALCHEMY_START_DB,
    connect_args={
        "check_same_thread": False
    }
)

# then create a sessionlocal class, of which each instance will be a db session
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
# autocommit=False means it won't auto commit, I will have to commit manually
# autoflush=False means it won't auto flush
# bind=engine means it will use the engine I created

# then create a Base class. I will inherit from this to create my database models.
class Base(DeclarativeBase):
    pass


# now that setup is complete I make my first db model
class URLStuff(Base):

    __tablename__ = "url_items"
    short_key: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    # using the random 5 characters as pk
    target_url: Mapped[str | None] = mapped_column(String, index=True)
    # the actual url I am shortening
