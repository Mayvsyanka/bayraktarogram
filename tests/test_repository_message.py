from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pytest

from src.database.models import Base, User, Message
from src.repository.message import send_message, read_messages, delete_messages

DATABASE_URL = "sqlite:///test.db"


@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.mark.asyncio
async def test_send_and_read_message(db: Session):
    sender = User(email="sender@example.com")
    db.add(sender)
    db.commit()

    receiver = User(email="receiver@example.com")
    db.add(receiver)
    db.commit()

    message_text = "Test message"
    message = await send_message(receiver, sender, message_text, db)
    assert message.text_message == message_text


    messages_sender = await read_messages(sender, db)
    assert len(messages_sender) == 1
    assert messages_sender[0].text_message == message_text

    messages_receiver = await read_messages(receiver, db)
    assert len(messages_receiver) == 1
    assert messages_receiver[0].text_message == message_text


@pytest.mark.asyncio
async def test_delete_message(db: Session):
    user = User(email="user@example.com")
    db.add(user)
    db.commit()

    sender = User(email="sender@example.com")
    db.add(sender)
    db.commit()
    message = await send_message(user, sender, "Test message", db)

    result = await delete_messages(message.id, user, db)
    assert result == f"Message with id: {message.id} does not exist"

    result = await delete_messages(message.id, sender, db)
    assert result is None

    messages_sender = await read_messages(sender, db)
    assert len(messages_sender) == 0
