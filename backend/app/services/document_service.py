from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(db: Session, *, user_id: UUID, title: str, content: str) -> Document:
    document = Document(user_id=user_id, title=title, content=content)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_documents(db: Session, *, user_id: UUID) -> list[Document]:
    statement = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
    return list(db.scalars(statement).all())


def get_document(db: Session, *, user_id: UUID, document_id: UUID) -> Document | None:
    statement = select(Document).where(Document.user_id == user_id, Document.id == document_id)
    return db.scalars(statement).first()


def delete_document(db: Session, *, user_id: UUID, document_id: UUID) -> bool:
    document = get_document(db, user_id=user_id, document_id=document_id)
    if document is None:
        return False

    db.delete(document)
    db.commit()
    return True