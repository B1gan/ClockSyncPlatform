from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.status_schema import StatusReportRequest, StatusResponse
from app.services.sync_service import report_status


router = APIRouter(tags=["status"])


@router.post("/status", response_model=StatusResponse)
def report_status_api(payload: StatusReportRequest, db: Session = Depends(get_db)):
    return report_status(db, payload)
