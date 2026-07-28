from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.document import DocumentCreate, DocumentRead
from app.services import document_service

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> DocumentRead:
    document = document_service.create_document(
        db,
        user_id=current_user.id,
        title=payload.title,
        content=payload.content,
    )
    return DocumentRead.model_validate(document)


@router.get("", response_model=list[DocumentRead])
def list_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[DocumentRead]:
    documents = document_service.list_documents(db, user_id=current_user.id)
    return [DocumentRead.model_validate(document) for document in documents]


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> DocumentRead:
    document = document_service.get_document(db, user_id=current_user.id, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return DocumentRead.model_validate(document)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> None:
    deleted = document_service.delete_document(db, user_id=current_user.id, document_id=document_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")