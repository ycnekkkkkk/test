from typing import Dict, Any
from app.services.gemini_service import GeminiService
from app.models.test_session import Level, Phase


class TestGeneratorService:
    """Service for generating IELTS test content using Gemini"""

    def __init__(self):
        self.gemini = GeminiService()

        self.level_to_band = {
            Level.BEGINNER: "3.0-4.0",
            Level.ELEMENTARY: "4.0-4.5",
            Level.INTERMEDIATE: "5.0-5.5",
            Level.UPPER_INTERMEDIATE: "6.0-6.5",
            Level.ADVANCED: "7.0-8.0",
        }

    def generate_listening_speaking(self, level: Level) -> Dict[str, Any]:
        """Generate Listening & Speaking test content (30 minutes)"""
        band = self.level_to_band.get(level, "5.0-5.5")

        system_instruction = """You are an expert IELTS examiner. Generate test content in JSON format only."""

        prompt = f"""Generate a 30-minute IELTS Listening & Speaking test for {level.value} level (estimated band {band}).

LISTENING SECTION (20 minutes):
- Section 1: Daily conversation (5 questions: multiple choice, fill-in-blank)
- Section 2: Social monologue (5 questions: multiple choice, matching)
- Section 3: Academic conversation (5 questions: multiple choice, short answer)
- Section 4: Academic lecture (5 questions: fill-in-blank, matching)

IMPORTANT: For each listening section, you MUST include a complete audio transcript that contains the full conversation, monologue, or lecture that students will listen to. The transcript should be natural, realistic, and contain all information needed to answer the questions.

SPEAKING SECTION (10 minutes):
- Part 1: 3-4 introduction questions (hometown, work/study, hobbies, family)
- Part 2: 1 topic card for 2-minute description
- Part 3: 3-4 discussion questions related to Part 2 topic

Return JSON format:
{{
    "listening": {{
        "sections": [
            {{
                "id": 1,
                "title": "Section 1: Daily Conversation",
                "instructions": "...",
                "audio_transcript": "Complete transcript of the conversation that students will listen to. Include all dialogue, pauses, and natural speech patterns. This should be 200-300 words for Section 1.",
                "questions": [
                    {{
                        "id": 1,
                        "type": "multiple_choice",
                        "question": "...",
                        "options": ["A. ...", "B. ...", "C. ..."],
                        "correct_answer": "A"
                    }},
                    {{
                        "id": 2,
                        "type": "fill_blank",
                        "question": "...",
                        "correct_answer": "..."
                    }}
                ]
            }}
        ]
    }},
    "speaking": {{
        "part1": [
            {{"id": 1, "question": "..."}},
            {{"id": 2, "question": "..."}}
        ],
        "part2": {{
            "topic": "...",
            "task_card": "..."
        }},
        "part3": [
            {{"id": 1, "question": "..."}}
        ]
    }}
}}"""

        return self.gemini.generate_json(prompt, system_instruction)

    def generate_reading_writing(self, level: Level) -> Dict[str, Any]:
        """Generate Reading & Writing test content (30 minutes)"""
        band = self.level_to_band.get(level, "5.0-5.5")

        system_instruction = """You are an expert IELTS examiner. Generate test content in JSON format only."""

        prompt = f"""Generate a 30-minute IELTS Reading & Writing test for {level.value} level (estimated band {band}).

READING SECTION (15 minutes):
- Passage 1: Data/chart-based article (300-400 words, 5 questions: multiple choice, True/False/Not Given)
- Passage 2: Social topic article (300-400 words, 5 questions: multiple choice, matching headings)

WRITING SECTION (15 minutes):
- Task 1: Describe a chart/graph (50-80 words) - provide detailed TEXT DESCRIPTION of the chart/graph data
- Task 2: Social essay topic (100-120 words) - provide essay question

IMPORTANT for Task 1: Since we cannot display actual charts, you MUST provide a detailed TEXT DESCRIPTION of the chart/graph that includes:
- Chart type (bar chart, line graph, pie chart, table, etc.)
- Title and what it shows
- All data points with specific numbers/percentages
- Categories, labels, and axes information
- Key trends, comparisons, or patterns visible in the data
The description should be comprehensive enough for students to write a complete Task 1 response without seeing the actual chart.

Return JSON format:
{{
    "reading": {{
        "passages": [
            {{
                "id": 1,
                "title": "...",
                "content": "...",
                "questions": [
                    {{
                        "id": 1,
                        "type": "multiple_choice",
                        "question": "...",
                        "options": ["A. ...", "B. ...", "C. ..."],
                        "correct_answer": "A"
                    }}
                ]
            }}
        ]
    }},
    "writing": {{
        "task1": {{
            "type": "chart_description",
            "instructions": "The [chart type] below shows [what it shows]. Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 50 words.",
            "chart_description": "DETAILED TEXT DESCRIPTION: [Chart type] titled '[Title]' showing [overview]. The data includes: [list all data points with numbers]. Key features: [trends/comparisons]. For example: Category A: X%, Category B: Y%, etc. [Include all necessary details for writing a complete response]",
            "word_count": 50
        }},
        "task2": {{
            "type": "essay",
            "question": "...",
            "word_count": 100
        }}
    }}
}}"""

        return self.gemini.generate_json(prompt, system_instruction)
