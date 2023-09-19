from sqlmodel import Session, create_engine


engine=create_engine("sqlite:///products.db",
                     connect_args={"check_same_thread":False},
                     echo=True)



def get_session():
    with Session(engine) as session:
            yield session


if __name__ == "__main__":
    get_session()