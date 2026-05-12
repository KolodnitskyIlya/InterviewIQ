from ml.base import RUBRIC_VERSION, RUBRIC_WEIGHTS, AnswerAnalysisInput, AnswerAnalysisResult

def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))

def weighted_score(scores: dict[str, float]) -> int:
    total = sum(scores[key] * weight for key, weight in RUBRIC_WEIGHTS.items())
    return round(clamp(total) * 100)

class BaselineAnalyzer:
    provider = "baseline"

    def analyze(self, payload: AnswerAnalysisInput) -> AnswerAnalysisResult:
        answer = (payload.transcript or payload.answer_text or "").strip()
        words = [word for word in answer.replace("\n", " ").split(" ") if word]
        word_count = len(words)
        lower = answer.lower()
        has_numbers = any(char.isdigit() for char in answer)
        has_structure_markers = any(
            marker in lower
            for marker in [
                "first",
                "second",
                "finally",
                "because",
                "result",
                "impact",
                "for example",
            ]
        )

        question_terms = {
            term.strip(".,?!:;").lower()
            for term in f"{payload.question_title} {payload.question_description}".split()
            if len(term.strip(".,?!:;")) >= 5
        }
        answer_terms = {term.strip(".,?!:;").lower() for term in words}
        overlap = len(question_terms & answer_terms)

        completeness = clamp(0.25 + min(0.55, word_count / 140) + (0.10 if payload.has_audio else 0.0))
        specificity = clamp(0.30 + (0.20 if has_numbers else 0.0) + min(0.35, word_count / 180))
        structure = clamp(0.35 + (0.25 if has_structure_markers else 0.0) + min(0.25, word_count / 220))
        relevance = clamp(0.45 + min(0.35, overlap * 0.07) + (0.10 if payload.category in lower else 0.0))
        confidence = clamp(0.45 + min(0.25, word_count / 220) - (0.10 if "maybe" in lower else 0.0))

        scores = {
            "structure": round(structure, 2),
            "relevance": round(relevance, 2),
            "specificity": round(specificity, 2),
            "confidence": round(confidence, 2),
            "completeness": round(completeness, 2),
        }

        strengths = []
        if relevance >= 0.70:
            strengths.append("Answer stays close to the question")
        if structure >= 0.65:
            strengths.append("Answer has a recognizable structure")
        if specificity >= 0.65:
            strengths.append("Answer includes concrete details")
        if not strengths:
            strengths.append("Relevant answer direction")

        to_improve = []
        if structure < 0.70:
            to_improve.append("Use a clearer structure with beginning, actions, and result")
        if specificity < 0.70:
            to_improve.append("Add one concrete metric, example, or trade-off")
        if completeness < 0.70:
            to_improve.append("Expand the answer with more context and impact")
        if not to_improve:
            to_improve.append("Make the final impact even more measurable")

        return AnswerAnalysisResult(
            overall_score=weighted_score(scores),
            scores_by_category=scores,
            strengths=strengths[:3],
            to_improve=to_improve[:3],
            quick_tips=[
                "Use STAR for behavioral answers or trade-offs for technical answers",
                "Add one measurable result",
                "Finish with impact",
            ],
            ideal_answer_example=(
                "I would start by clarifying the goal and constraints, then explain the main approach, "
                "trade-offs, and measurable impact. For example, I would describe what changed, why it "
                "worked, and how I verified the result."
            ),
            explanation="Baseline rubric score based on answer length, structure markers, relevance, and specificity.",
            provider=self.provider,
            rubric_version=RUBRIC_VERSION,
        )
