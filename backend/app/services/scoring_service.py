from typing import Dict, Any
from app.services.gemini_service import GeminiService
from app.models.test_session import Phase
import json


class ScoringService:
    """Service for scoring test phases using Gemini"""

    # IELTS Band conversion tables (standard IELTS conversion)
    LISTENING_BANDS = {
        0: 2.5,
        1: 2.5,
        2: 2.5,
        3: 2.5,
        4: 2.5,
        5: 3.0,
        6: 3.0,
        7: 3.5,
        8: 3.5,
        9: 3.5,
        10: 4.0,
        11: 4.0,
        12: 4.0,
        13: 4.5,
        14: 4.5,
        15: 4.5,
        16: 5.0,
        17: 5.0,
        18: 5.5,
        19: 5.5,
        20: 5.5,
        21: 5.5,
        22: 5.5,
        23: 6.0,
        24: 6.0,
        25: 6.0,
        26: 6.5,
        27: 6.5,
        28: 6.5,
        29: 6.5,
        30: 7.0,
        31: 7.0,
        32: 7.5,
        33: 7.5,
        34: 7.5,
        35: 8.0,
        36: 8.0,
        37: 8.5,
        38: 8.5,
        39: 9.0,
        40: 9.0,
    }

    READING_BANDS = {
        0: 2.5,
        1: 2.5,
        2: 2.5,
        3: 2.5,
        4: 2.5,
        5: 3.0,
        6: 3.0,
        7: 3.5,
        8: 3.5,
        9: 3.5,
        10: 4.0,
        11: 4.0,
        12: 4.0,
        13: 4.5,
        14: 4.5,
        15: 5.0,
        16: 5.0,
        17: 5.0,
        18: 5.0,
        19: 5.5,
        20: 5.5,
        21: 5.5,
        22: 5.5,
        23: 6.0,
        24: 6.0,
        25: 6.0,
        26: 6.0,
        27: 6.5,
        28: 6.5,
        29: 6.5,
        30: 7.0,
        31: 7.0,
        32: 7.0,
        33: 7.5,
        34: 7.5,
        35: 8.0,
        36: 8.0,
        37: 8.5,
        38: 8.5,
        39: 9.0,
        40: 9.0,
    }

    def __init__(self):
        self.gemini = GeminiService()

    def score_listening(
        self, content: Dict[str, Any], answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Score Listening section (objective questions)"""
        correct_count = 0
        total_questions = 0
        detailed_results = []

        sections = content.get("listening", {}).get("sections", [])
        for section in sections:
            section_id = section.get("id")
            questions = section.get("questions", [])

            for question in questions:
                qid = question.get("id")
                total_questions += 1
                user_answer = answers.get(f"listening_s{section_id}_q{qid}", "").strip()
                correct_answer = str(question.get("correct_answer", "")).strip()

                is_correct = user_answer.lower() == correct_answer.lower()
                if is_correct:
                    correct_count += 1

                detailed_results.append(
                    {
                        "question_id": qid,
                        "section_id": section_id,
                        "user_answer": user_answer,
                        "correct_answer": correct_answer,
                        "is_correct": is_correct,
                    }
                )

        raw_score = correct_count

        # Check if user provided any answers
        has_any_answer = any(
            answers.get(f"listening_s{section.get('id')}_q{q.get('id')}", "").strip()
            for section in sections
            for q in section.get("questions", [])
        )

        # Logic:
        # - No answers → 0.0
        # - Has answers but all wrong (raw_score = 0) → 0.0
        # - Has answers and some correct (raw_score > 0) → use band table
        if not has_any_answer:
            band = 0.0
        elif raw_score == 0:
            band = 0.0  # Answered but all wrong = 0.0 (not 2.5)
        else:
            band = self.LISTENING_BANDS.get(raw_score, 0.0)

        return {
            "raw_score": raw_score,
            "total_questions": total_questions,
            "band": round(band, 1),
            "detailed_results": detailed_results,
        }

    def score_reading(
        self, content: Dict[str, Any], answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Score Reading section (objective questions)"""
        correct_count = 0
        total_questions = 0
        detailed_results = []

        passages = content.get("reading", {}).get("passages", [])
        for passage in passages:
            passage_id = passage.get("id")
            questions = passage.get("questions", [])

            for question in questions:
                qid = question.get("id")
                total_questions += 1
                user_answer = answers.get(f"reading_p{passage_id}_q{qid}", "").strip()
                correct_answer = str(question.get("correct_answer", "")).strip()

                is_correct = user_answer.lower() == correct_answer.lower()
                if is_correct:
                    correct_count += 1

                detailed_results.append(
                    {
                        "question_id": qid,
                        "passage_id": passage_id,
                        "user_answer": user_answer,
                        "correct_answer": correct_answer,
                        "is_correct": is_correct,
                    }
                )

        raw_score = correct_count

        # Check if user provided any answers
        has_any_answer = any(
            answers.get(f"reading_p{passage.get('id')}_q{q.get('id')}", "").strip()
            for passage in passages
            for q in passage.get("questions", [])
        )

        # Logic:
        # - No answers → 0.0
        # - Has answers but all wrong (raw_score = 0) → 0.0
        # - Has answers and some correct (raw_score > 0) → use band table
        if not has_any_answer:
            band = 0.0
        elif raw_score == 0:
            band = 0.0  # Answered but all wrong = 0.0 (not 2.5)
        else:
            band = self.READING_BANDS.get(raw_score, 0.0)

        return {
            "raw_score": raw_score,
            "total_questions": total_questions,
            "band": round(band, 1),
            "detailed_results": detailed_results,
        }

    def score_speaking(
        self, content: Dict[str, Any], answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Score Speaking section using Gemini (4 IELTS criteria) - Optimized for token limits"""
        # Check if user provided any answers
        part1_questions = content.get("speaking", {}).get("part1", [])
        part2 = content.get("speaking", {}).get("part2", {})
        part3_questions = content.get("speaking", {}).get("part3", [])

        # Collect all answer keys
        all_answer_keys = []
        for q in part1_questions:
            all_answer_keys.append(f"speaking_part1_{q.get('id')}")
        if part2:
            all_answer_keys.append("speaking_part2")
        for q in part3_questions:
            all_answer_keys.append(f"speaking_part3_{q.get('id')}")

        # Check if any answer exists and is not empty
        has_any_answer = any(answers.get(key, "").strip() for key in all_answer_keys)

        # If no answers provided, return 0.0 scores
        if not has_any_answer:
            return {
                "fluency_coherence": 0.0,
                "lexical_resource": 0.0,
                "grammatical_range": 0.0,
                "pronunciation": 0.0,
                "overall_band": 0.0,
                "feedback": "No answers provided",
            }

        system_instruction = """You are an IELTS examiner. Evaluate speaking using 4 criteria: Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, Pronunciation. Return JSON only."""

        def truncate_text(text: str, max_words: int = 100) -> str:
            """Truncate text to max words to reduce token usage"""
            if not text:
                return ""
            words = text.split()
            if len(words) <= max_words:
                return text
            return " ".join(words[:max_words]) + "..."

        # Extract part 1 answers (keys like speaking_part1_1, speaking_part1_2, etc.)
        part1_questions = content.get("speaking", {}).get("part1", [])
        part1_answers_dict = {}
        for q in part1_questions:
            qid = q.get("id")
            answer_key = f"speaking_part1_{qid}"
            if answer_key in answers:
                part1_answers_dict[qid] = answers[answer_key]

        # Extract part 2 answer
        speaking_part2_answer = answers.get("speaking_part2", "")

        # Extract part 3 answers (keys like speaking_part3_1, speaking_part3_2, etc.)
        part3_questions = content.get("speaking", {}).get("part3", [])
        part3_answers_dict = {}
        for q in part3_questions:
            qid = q.get("id")
            answer_key = f"speaking_part3_{qid}"
            if answer_key in answers:
                part3_answers_dict[qid] = answers[answer_key]

        part2 = content.get("speaking", {}).get("part2", {})

        # Truncate part2 answer to reduce token usage
        speaking_part2_answer = truncate_text(speaking_part2_answer, max_words=200)

        # Build optimized prompt - shorter format, limit questions
        part1_items = []
        for q in part1_questions[:4]:  # Limit to first 4 questions
            qid = q.get("id")
            q_text = q.get("question", "")[:100]  # Limit question length
            a_text = truncate_text(part1_answers_dict.get(qid, ""), 50)
            part1_items.append(f"Q{qid}: {q_text}\nA: {a_text}")
        part1_text = "\n".join(part1_items)

        part3_items = []
        for q in part3_questions[:4]:  # Limit to first 4 questions
            qid = q.get("id")
            q_text = q.get("question", "")[:100]  # Limit question length
            a_text = truncate_text(part3_answers_dict.get(qid, ""), 80)
            part3_items.append(f"Q{qid}: {q_text}\nA: {a_text}")
        part3_text = "\n".join(part3_items)

        # Optimized prompt - shorter and more focused
        task_card = part2.get("task_card", "")[:200]  # Limit task card length
        prompt = f"""Evaluate IELTS Speaking:

P1: {part1_text}

P2: {task_card}
A2: {speaking_part2_answer}

P3: {part3_text}

Return JSON only:
{{"fluency_coherence":7.0,"lexical_resource":7.0,"grammatical_range":7.0,"pronunciation":7.0,"overall_band":7.0,"feedback":"Brief feedback"}}"""

        try:
            print("Calling Gemini API for Speaking scoring...")
            result = self.gemini.generate_json(prompt, system_instruction)
            print("Gemini API response received for Speaking")
            return {
                "fluency_coherence": result.get("fluency_coherence", 5.0),
                "lexical_resource": result.get("lexical_resource", 5.0),
                "grammatical_range": result.get("grammatical_range", 5.0),
                "pronunciation": result.get("pronunciation", 5.0),
                "overall_band": result.get("overall_band", 5.0),
                "feedback": result.get("feedback", ""),
            }
        except Exception as e:
            print(f"Speaking scoring error: {e}")
            import traceback

            print(traceback.format_exc())
            # Fallback scores
            return {
                "fluency_coherence": 5.0,
                "lexical_resource": 5.0,
                "grammatical_range": 5.0,
                "pronunciation": 5.0,
                "overall_band": 5.0,
                "feedback": "Không thể đánh giá tự động",
            }

    def score_writing(
        self, content: Dict[str, Any], answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Score Writing section using Gemini (4 IELTS criteria) - Optimized for token limits"""
        task1_answer = answers.get("writing_task1", "").strip()
        task2_answer = answers.get("writing_task2", "").strip()

        # Check if user provided any answers
        has_any_answer = bool(task1_answer or task2_answer)

        # If no answers provided, return 0.0 scores
        if not has_any_answer:
            return {
                "task1": {
                    "task_achievement": 0.0,
                    "coherence_cohesion": 0.0,
                    "lexical_resource": 0.0,
                    "grammatical_range": 0.0,
                    "overall_band": 0.0,
                },
                "task2": {
                    "task_response": 0.0,
                    "coherence_cohesion": 0.0,
                    "lexical_resource": 0.0,
                    "grammatical_range": 0.0,
                    "overall_band": 0.0,
                },
                "overall_band": 0.0,
                "feedback": "No answers provided",
            }

        system_instruction = """You are an IELTS examiner. Evaluate writing using 4 criteria: Task Achievement/Response, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy. Return JSON only."""

        def truncate_text(text: str, max_words: int = 150) -> str:
            """Truncate text to max words to reduce token usage"""
            if not text:
                return ""
            words = text.split()
            if len(words) <= max_words:
                return text
            return " ".join(words[:max_words]) + "..."

        # Truncate answers to reduce token usage (Task 1: 50-80 words, Task 2: 100-120 words expected)
        task1_answer = truncate_text(task1_answer, max_words=100)
        task2_answer = truncate_text(task2_answer, max_words=150)

        task1_instructions = (
            content.get("writing", {}).get("task1", {}).get("instructions", "")
        )
        # Don't include chart_description to save tokens - instructions are enough
        task2_question = content.get("writing", {}).get("task2", {}).get("question", "")

        # Optimized prompt - shorter and more focused
        prompt = f"""Evaluate IELTS Writing:

T1: {task1_instructions}
A1: {task1_answer}

T2: {task2_question}
A2: {task2_answer}

Return JSON only:
{{"task1":{{"task_achievement":7.0,"coherence_cohesion":7.0,"lexical_resource":7.0,"grammatical_range":7.0,"overall_band":7.0}},"task2":{{"task_response":7.0,"coherence_cohesion":7.0,"lexical_resource":7.0,"grammatical_range":7.0,"overall_band":7.0}},"overall_band":7.0,"feedback":"Brief feedback"}}"""

        try:
            print("Calling Gemini API for Writing scoring...")
            result = self.gemini.generate_json(prompt, system_instruction)
            print("Gemini API response received for Writing")
            task1_scores = result.get("task1", {})
            task2_scores = result.get("task2", {})

            return {
                "task1": {
                    "task_achievement": task1_scores.get("task_achievement", 5.0),
                    "coherence_cohesion": task1_scores.get("coherence_cohesion", 5.0),
                    "lexical_resource": task1_scores.get("lexical_resource", 5.0),
                    "grammatical_range": task1_scores.get("grammatical_range", 5.0),
                    "overall_band": task1_scores.get("overall_band", 5.0),
                },
                "task2": {
                    "task_response": task2_scores.get("task_response", 5.0),
                    "coherence_cohesion": task2_scores.get("coherence_cohesion", 5.0),
                    "lexical_resource": task2_scores.get("lexical_resource", 5.0),
                    "grammatical_range": task2_scores.get("grammatical_range", 5.0),
                    "overall_band": task2_scores.get("overall_band", 5.0),
                },
                "overall_band": result.get("overall_band", 5.0),
                "feedback": result.get("feedback", ""),
            }
        except Exception as e:
            print(f"Writing scoring error: {e}")
            import traceback

            print(traceback.format_exc())
            # Fallback scores
            return {
                "task1": {
                    "task_achievement": 5.0,
                    "coherence_cohesion": 5.0,
                    "lexical_resource": 5.0,
                    "grammatical_range": 5.0,
                    "overall_band": 5.0,
                },
                "task2": {
                    "task_response": 5.0,
                    "coherence_cohesion": 5.0,
                    "lexical_resource": 5.0,
                    "grammatical_range": 5.0,
                    "overall_band": 5.0,
                },
                "overall_band": 5.0,
                "feedback": "Không thể đánh giá tự động",
            }

    def aggregate_results(
        self,
        phase1_scores: Dict[str, Any],
        phase2_scores: Dict[str, Any],
        phase1_type: Phase,
        phase2_type: Phase,
    ) -> Dict[str, Any]:
        """Aggregate final IELTS results from both phases"""
        results = {
            "listening": 0.0,
            "reading": 0.0,
            "writing": 0.0,
            "speaking": 0.0,
        }

        # Extract scores from phase 1
        if phase1_type == Phase.LISTENING_SPEAKING:
            results["listening"] = phase1_scores.get("listening", {}).get("band", 0.0)
            results["speaking"] = phase1_scores.get("speaking", {}).get(
                "overall_band", 0.0
            )
        elif phase1_type == Phase.READING_WRITING:
            results["reading"] = phase1_scores.get("reading", {}).get("band", 0.0)
            results["writing"] = phase1_scores.get("writing", {}).get(
                "overall_band", 0.0
            )

        # Extract scores from phase 2
        if phase2_type == Phase.LISTENING_SPEAKING:
            results["listening"] = phase2_scores.get("listening", {}).get("band", 0.0)
            results["speaking"] = phase2_scores.get("speaking", {}).get(
                "overall_band", 0.0
            )
        elif phase2_type == Phase.READING_WRITING:
            results["reading"] = phase2_scores.get("reading", {}).get("band", 0.0)
            results["writing"] = phase2_scores.get("writing", {}).get(
                "overall_band", 0.0
            )

        # Calculate overall band (average of 4 skills)
        overall = round(
            (
                results["listening"]
                + results["reading"]
                + results["writing"]
                + results["speaking"]
            )
            / 4.0,
            1,
        )

        results["overall"] = overall

        return results

    def generate_detailed_analysis(
        self,
        phase1_scores: Dict[str, Any],
        phase2_scores: Dict[str, Any],
        phase1_type: Phase,
        phase2_type: Phase,
        phase1_content: Dict[str, Any],
        phase2_content: Dict[str, Any],
        phase1_answers: Dict[str, Any],
        phase2_answers: Dict[str, Any],
        final_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate detailed analysis including IELTS framework and beyond-IELTS insights - Optimized for token limits"""
        system_instruction = (
            """Giám khảo IELTS. Phân tích tiếng Anh. Trả về TIẾNG VIỆT. Chỉ JSON."""
        )

        # Prepare data for analysis
        listening_score = final_results.get("listening", 0)
        reading_score = final_results.get("reading", 0)
        writing_score = final_results.get("writing", 0)
        speaking_score = final_results.get("speaking", 0)
        overall_score = final_results.get("overall", 0)

        # Collect summaries (compact format - direct extraction)
        listening_summary = ""
        reading_summary = ""

        if phase1_type == Phase.LISTENING_SPEAKING and phase1_scores.get("listening"):
            l1 = phase1_scores["listening"]
            listening_summary += f"P1:{l1.get('raw_score', 0)}/{l1.get('total_questions', 0)}={l1.get('band', 0):.1f} "
        if phase2_type == Phase.LISTENING_SPEAKING and phase2_scores.get("listening"):
            l2 = phase2_scores["listening"]
            listening_summary += f"P2:{l2.get('raw_score', 0)}/{l2.get('total_questions', 0)}={l2.get('band', 0):.1f}"

        if phase1_type == Phase.READING_WRITING and phase1_scores.get("reading"):
            r1 = phase1_scores["reading"]
            reading_summary += f"P1:{r1.get('raw_score', 0)}/{r1.get('total_questions', 0)}={r1.get('band', 0):.1f} "
        if phase2_type == Phase.READING_WRITING and phase2_scores.get("reading"):
            r2 = phase2_scores["reading"]
            reading_summary += f"P2:{r2.get('raw_score', 0)}/{r2.get('total_questions', 0)}={r2.get('band', 0):.1f}"

        # Compact summaries
        writing_summary = ""
        if phase1_scores.get("writing"):
            w1 = phase1_scores["writing"]
            writing_summary += f"P1:T1={w1.get('task1', {}).get('overall_band', 0):.1f} T2={w1.get('task2', {}).get('overall_band', 0):.1f} O={w1.get('overall_band', 0):.1f} "
        if phase2_scores.get("writing"):
            w2 = phase2_scores["writing"]
            writing_summary += f"P2:T1={w2.get('task1', {}).get('overall_band', 0):.1f} T2={w2.get('task2', {}).get('overall_band', 0):.1f} O={w2.get('overall_band', 0):.1f}"

        speaking_summary = ""
        if phase1_scores.get("speaking"):
            s1 = phase1_scores["speaking"]
            speaking_summary += f"P1:FC={s1.get('fluency_coherence', 0):.1f} LR={s1.get('lexical_resource', 0):.1f} GR={s1.get('grammatical_range', 0):.1f} P={s1.get('pronunciation', 0):.1f} O={s1.get('overall_band', 0):.1f} "
        if phase2_scores.get("speaking"):
            s2 = phase2_scores["speaking"]
            speaking_summary += f"P2:FC={s2.get('fluency_coherence', 0):.1f} LR={s2.get('lexical_resource', 0):.1f} GR={s2.get('grammatical_range', 0):.1f} P={s2.get('pronunciation', 0):.1f} O={s2.get('overall_band', 0):.1f}"

        # Sample answers for analysis (reduced to save tokens)
        def sample_answer(text: str, max_words: int = 20) -> str:
            if not text:
                return ""
            words = text.split()
            if len(words) <= max_words:
                return text
            return " ".join(words[:max_words]) + "..."

        # Reduce samples further to save tokens
        writing_samples = ""
        if phase1_answers.get("writing_task2"):
            writing_samples += (
                f"W1:{sample_answer(phase1_answers['writing_task2'], 15)} "
            )
        if phase2_answers.get("writing_task2"):
            writing_samples += (
                f"W2:{sample_answer(phase2_answers['writing_task2'], 15)}"
            )

        # Only 1 speaking sample total
        speaking_samples = ""
        for key in list(phase1_answers.keys()):
            if key.startswith("speaking_"):
                speaking_samples += f"S1:{sample_answer(phase1_answers[key], 15)}"
                break
        if not speaking_samples:
            for key in list(phase2_answers.keys()):
                if key.startswith("speaking_"):
                    speaking_samples += f"S2:{sample_answer(phase2_answers[key], 15)}"
                    break

        # Split into 2 separate API calls: Key 1 for IELTS, Key 2 for Beyond IELTS
        ielts_analysis = {}
        beyond_ielts = {}

        # Part 1: IELTS Analysis using Key 1 (ultra-compact Vietnamese)
        ielts_prompt = f"""IELTS (TIẾNG VIỆT):

Scores: L={listening_score:.1f} R={reading_score:.1f} W={writing_score:.1f} S={speaking_score:.1f} O={overall_score:.1f}
Data: L:{listening_summary if listening_summary else 'N/A'} R:{reading_summary if reading_summary else 'N/A'} W:{writing_summary if writing_summary else 'N/A'} S:{speaking_summary if speaking_summary else 'N/A'}
Samples: W:{writing_samples[:80] if writing_samples else 'N/A'} S:{speaking_samples[:80] if speaking_samples else 'N/A'}

Phân tích (TIẾNG VIỆT):
- R: mạnh/yếu, dạng câu (MC,T/F/NG,matching,fill-blank)
- L: mạnh/yếu, dạng câu (MC,fill-blank,matching,short)
- W: 4 tiêu chí (TA,CC,LR,GR) - mạnh/yếu từng tiêu chí, T1 vs T2
- S: 4 tiêu chí (FC,LR,GR,P) - mạnh/yếu từng tiêu chí

JSON (TIẾNG VIỆT): {{"ielts_analysis":{{"reading":{{"strengths":[],"weaknesses":[],"question_type_analysis":{{}}}}, "listening":{{"strengths":[],"weaknesses":[],"question_type_analysis":{{}}}}, "writing":{{"task_achievement":{{"score":0,"strengths":[],"weaknesses":[]}}, "coherence_cohesion":{{"score":0,"strengths":[],"weaknesses":[]}}, "lexical_resource":{{"score":0,"strengths":[],"weaknesses":[]}}, "grammatical_range":{{"score":0,"strengths":[],"weaknesses":[]}}, "overall_assessment":""}}, "speaking":{{"fluency_coherence":{{"score":0,"strengths":[],"weaknesses":[]}}, "lexical_resource":{{"score":0,"strengths":[],"weaknesses":[]}}, "grammatical_range":{{"score":0,"strengths":[],"weaknesses":[]}}, "pronunciation":{{"score":0,"strengths":[],"weaknesses":[]}}, "overall_assessment":""}}}}}}"""

        # Part 2: Beyond IELTS Analysis using Key 2 (ultra-compact Vietnamese)
        beyond_prompt = f"""Beyond IELTS (TIẾNG VIỆT):

Scores: L={listening_score:.1f} R={reading_score:.1f} W={writing_score:.1f} S={speaking_score:.1f} O={overall_score:.1f}
Data: W:{writing_summary if writing_summary else 'N/A'} S:{speaking_summary if speaking_summary else 'N/A'}
Samples: W:{writing_samples[:80] if writing_samples else 'N/A'} S:{speaking_samples[:80] if speaking_samples else 'N/A'}

Phân tích (TIẾNG VIỆT):
- Phản xạ: thấp/trung bình/cao
- Tiếp thu: khả năng tiếp thu xử lý thông tin
- Ngôn ngữ mẹ đẻ: dịch, từ vựng (tự nhiên/dịch máy), tác động L/R/S/W
- Văn phạm: lỗi nghĩa, lỗi văn phạm, cấu trúc, không tự nhiên
- Phát âm: rõ ràng, mạch lạc, nghe native, nhịp/nhấn, chính xác từ, âm đôi/đuôi
- Từ vựng: mức (cơ bản/nâng cao), tự nhiên/dịch, đánh giá

JSON (TIẾNG VIỆT): {{"beyond_ielts":{{"reflex_level":"","reception_ability":"","mother_tongue_influence":{{"translation":"","vocabulary_usage":"","listening":"","reading":"","speaking":"","writing":""}}, "grammar":{{"meaning_errors":"","grammar_errors":"","structure_errors":"","unnatural":""}}, "pronunciation":{{"hard_to_understand":"","lack_coherence":"","native_comprehension":"","rhythm_stress":"","word_pronunciation":"","diphthongs_endings":""}}, "vocabulary":{{"level":"","natural_vs_translated":"","assessment":""}}}}}}"""

        try:
            print("Generating IELTS analysis (using Key 1)...")
            ielts_result = self.gemini.generate_json(
                ielts_prompt, system_instruction, force_key=1
            )
            ielts_analysis = ielts_result.get("ielts_analysis", {})
            print("IELTS analysis generated successfully")
        except Exception as e:
            print(f"Error generating IELTS analysis: {e}")
            ielts_analysis = {}

        try:
            print("Generating Beyond IELTS analysis (using Key 2)...")
            beyond_result = self.gemini.generate_json(
                beyond_prompt, system_instruction, force_key=2
            )
            beyond_ielts = beyond_result.get("beyond_ielts", {})
            print("Beyond IELTS analysis generated successfully")
        except Exception as e:
            print(f"Error generating Beyond IELTS analysis: {e}")
            beyond_ielts = {}

        return {"ielts_analysis": ielts_analysis, "beyond_ielts": beyond_ielts}
