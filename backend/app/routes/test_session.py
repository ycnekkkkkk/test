from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from app.database import get_db
from app.models.test_session import TestSession, Level, Phase, SessionStatus
from app.schemas.test_session import (
    SessionCreate,
    SessionResponse,
    PhaseSelection,
    AnswersSubmit,
    SessionStatusResponse,
)
from app.services.test_generator import TestGeneratorService
from app.services.scoring_service import ScoringService

router = APIRouter()

test_generator = TestGeneratorService()
scoring_service = ScoringService()


@router.post("/sessions", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """1. Khởi tạo: Tạo test_session với level"""
    session = TestSession(level=session_data.level, status=SessionStatus.INITIALIZED)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/sessions/{session_id}/select-phase", response_model=SessionResponse)
def select_phase(
    session_id: int, phase_data: PhaseSelection, db: Session = Depends(get_db)
):
    """2. Chọn phần làm trước: User chọn phase (Listening & Speaking hoặc Reading & Writing)"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != SessionStatus.INITIALIZED:
        raise HTTPException(status_code=400, detail="Phase already selected")

    session.selected_phase = phase_data.phase
    session.status = SessionStatus.PHASE1_SELECTED
    db.commit()
    db.refresh(session)
    return session


@router.post("/sessions/{session_id}/generate", response_model=SessionResponse)
def generate_phase_content(session_id: int, db: Session = Depends(get_db)):
    """3. Generate đề: Tạo đề cho phase đã chọn (chỉ gọi AI 1 lần)"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.selected_phase:
        raise HTTPException(status_code=400, detail="Please select a phase first")

    # Check if phase 1 already generated
    if session.phase1_content:
        return session

    # Generate content for selected phase
    try:
        if session.selected_phase == Phase.LISTENING_SPEAKING:
            content = test_generator.generate_listening_speaking(session.level)
        elif session.selected_phase == Phase.READING_WRITING:
            content = test_generator.generate_reading_writing(session.level)
        else:
            raise HTTPException(status_code=400, detail="Invalid phase")

        session.phase1_content = content
        session.status = SessionStatus.PHASE1_GENERATED
        db.commit()
        db.refresh(session)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin session"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/sessions/{session_id}/start-phase1")
def start_phase1(session_id: int, db: Session = Depends(get_db)):
    """Bắt đầu làm phase 1"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.phase1_content:
        raise HTTPException(status_code=400, detail="Phase 1 content not generated")

    session.status = SessionStatus.PHASE1_IN_PROGRESS
    session.phase1_started_at = datetime.now()
    db.commit()
    return {"message": "Phase 1 started", "session_id": session_id}


@router.post("/sessions/{session_id}/submit-phase1", response_model=SessionResponse)
def submit_phase1(
    session_id: int, answers: AnswersSubmit, db: Session = Depends(get_db)
):
    """5. Nộp bài phase 1: AI chấm điểm và lưu kết quả"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.phase1_content:
        raise HTTPException(status_code=400, detail="Phase 1 content not generated")

    session.phase1_answers = answers.answers
    session.phase1_completed_at = datetime.now()

    # Score phase 1
    try:
        scores = {}
        print(f"Starting scoring for phase 1, selected_phase: {session.selected_phase}")

        if session.selected_phase == Phase.LISTENING_SPEAKING:
            print("Scoring Listening & Speaking...")
            scores["listening"] = scoring_service.score_listening(
                session.phase1_content, answers.answers
            )
            print("Listening scored, starting Speaking...")
            scores["speaking"] = scoring_service.score_speaking(
                session.phase1_content, answers.answers
            )
            print("Speaking scored")
        elif session.selected_phase == Phase.READING_WRITING:
            print("Scoring Reading & Writing...")
            scores["reading"] = scoring_service.score_reading(
                session.phase1_content, answers.answers
            )
            print("Reading scored, starting Writing...")
            scores["writing"] = scoring_service.score_writing(
                session.phase1_content, answers.answers
            )
            print("Writing scored")

        session.phase1_scores = scores
        session.status = SessionStatus.PHASE1_COMPLETED
        db.commit()
        db.refresh(session)
        print(f"Phase 1 scoring completed successfully")
        return session
    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        print(f"Scoring error: {error_details}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Scoring error: {str(e)}")


@router.post("/sessions/{session_id}/generate-phase2", response_model=SessionResponse)
def generate_phase2(session_id: int, db: Session = Depends(get_db)):
    """6. Generate phase 2: Tạo đề cho phase còn lại"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != SessionStatus.PHASE1_COMPLETED:
        raise HTTPException(status_code=400, detail="Please complete phase 1 first")

    if session.phase2_content:
        return session

    # Determine phase 2 type
    phase2_type = (
        Phase.READING_WRITING
        if session.selected_phase == Phase.LISTENING_SPEAKING
        else Phase.LISTENING_SPEAKING
    )

    # Generate phase 2 content
    try:
        if phase2_type == Phase.LISTENING_SPEAKING:
            content = test_generator.generate_listening_speaking(session.level)
        else:
            content = test_generator.generate_reading_writing(session.level)

        session.phase2_content = content
        session.status = SessionStatus.PHASE2_GENERATED
        db.commit()
        db.refresh(session)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")


@router.post("/sessions/{session_id}/start-phase2")
def start_phase2(session_id: int, db: Session = Depends(get_db)):
    """Bắt đầu làm phase 2"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.phase2_content:
        raise HTTPException(status_code=400, detail="Phase 2 content not generated")

    session.status = SessionStatus.PHASE2_IN_PROGRESS
    session.phase2_started_at = datetime.now()
    db.commit()
    return {"message": "Phase 2 started", "session_id": session_id}


@router.post("/sessions/{session_id}/submit-phase2", response_model=SessionResponse)
def submit_phase2(
    session_id: int, answers: AnswersSubmit, db: Session = Depends(get_db)
):
    """7. Nộp bài phase 2: AI chấm điểm phase 2"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.phase2_content:
        raise HTTPException(status_code=400, detail="Phase 2 content not generated")

    session.phase2_answers = answers.answers
    session.phase2_completed_at = datetime.now()

    # Score phase 2
    try:
        scores = {}
        phase2_type = (
            Phase.READING_WRITING
            if session.selected_phase == Phase.LISTENING_SPEAKING
            else Phase.LISTENING_SPEAKING
        )

        if phase2_type == Phase.LISTENING_SPEAKING:
            scores["listening"] = scoring_service.score_listening(
                session.phase2_content, answers.answers
            )
            scores["speaking"] = scoring_service.score_speaking(
                session.phase2_content, answers.answers
            )
        else:
            scores["reading"] = scoring_service.score_reading(
                session.phase2_content, answers.answers
            )
            scores["writing"] = scoring_service.score_writing(
                session.phase2_content, answers.answers
            )

        session.phase2_scores = scores
        session.status = SessionStatus.PHASE2_COMPLETED
        db.commit()
        db.refresh(session)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring error: {str(e)}")


@router.post("/sessions/{session_id}/aggregate", response_model=SessionResponse)
def aggregate_results(session_id: int, db: Session = Depends(get_db)):
    """8. Tổng hợp kết quả: Tính IELTS equivalent và phân tích"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != SessionStatus.PHASE2_COMPLETED:
        raise HTTPException(status_code=400, detail="Please complete both phases first")

    if session.final_results:
        return session

    # Aggregate results
    phase2_type = (
        Phase.READING_WRITING
        if session.selected_phase == Phase.LISTENING_SPEAKING
        else Phase.LISTENING_SPEAKING
    )

    final_results = scoring_service.aggregate_results(
        session.phase1_scores,
        session.phase2_scores,
        session.selected_phase,
        phase2_type,
    )

    # Generate detailed analysis (optimized to reduce token usage)
    try:
        print("Generating detailed analysis...")
        detailed_analysis = scoring_service.generate_detailed_analysis(
            session.phase1_scores or {},
            session.phase2_scores or {},
            session.selected_phase,
            phase2_type,
            session.phase1_content or {},
            session.phase2_content or {},
            session.phase1_answers or {},
            session.phase2_answers or {},
            final_results,
        )
        final_results["detailed_analysis"] = detailed_analysis
        print("Detailed analysis generated successfully")
    except Exception as e:
        print(f"Error generating detailed analysis (non-critical): {e}")
        # Continue without analysis - it's optional
        final_results["detailed_analysis"] = {"ielts_analysis": {}, "beyond_ielts": {}}

    session.final_results = final_results
    session.status = SessionStatus.COMPLETED
    db.commit()
    db.refresh(session)
    return session


@router.post("/sessions/{session_id}/generate-analysis", response_model=SessionResponse)
def generate_detailed_analysis_endpoint(session_id: int, db: Session = Depends(get_db)):
    """Generate detailed analysis (call this after displaying basic results)"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.final_results:
        raise HTTPException(status_code=400, detail="Please aggregate results first")

    # Check if analysis already exists
    if session.final_results.get("detailed_analysis"):
        return session

    phase2_type = (
        Phase.READING_WRITING
        if session.selected_phase == Phase.LISTENING_SPEAKING
        else Phase.LISTENING_SPEAKING
    )

    # Generate detailed analysis
    try:
        detailed_analysis = scoring_service.generate_detailed_analysis(
            session.phase1_scores,
            session.phase2_scores,
            session.selected_phase,
            phase2_type,
            session.phase1_content,
            session.phase2_content,
            session.phase1_answers or {},
            session.phase2_answers or {},
            session.final_results,
        )

        # Add detailed analysis to final results
        session.final_results["detailed_analysis"] = detailed_analysis
        db.commit()
        db.refresh(session)
        return session
    except Exception as e:
        # Log error but don't fail - analysis is optional
        print(f"Error generating detailed analysis: {e}")
        # Return session without analysis
        return session


@router.get("/sessions/{session_id}/status", response_model=SessionStatusResponse)
def get_session_status(session_id: int, db: Session = Depends(get_db)):
    """Lấy trạng thái session"""
    session = db.query(TestSession).filter(TestSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionStatusResponse(
        id=session.id,
        status=session.status,
        level=session.level,
        selected_phase=session.selected_phase,
        phase1_available=session.phase1_content is not None,
        phase2_available=session.phase2_content is not None,
        phase1_completed=session.phase1_scores is not None,
        phase2_completed=session.phase2_scores is not None,
    )
