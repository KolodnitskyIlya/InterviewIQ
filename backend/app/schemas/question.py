from pydantic import BaseModel


class QuestionItem(BaseModel):
    id: str
    category: str
    difficulty: str
    title: str
    description: str


class QuestionsResponse(BaseModel):
    items: list[QuestionItem]


class SessionQuestionResponse(BaseModel):
    session_id: str
    current_question_index: int
    total_questions: int
    question: QuestionItem | None
