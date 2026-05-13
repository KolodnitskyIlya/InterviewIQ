ANALYSIS_SYSTEM_PROMPT = """
You are an interview coach. Evaluate the candidate answer using the rubric.
Return only valid JSON matching the requested schema. Do not include markdown.
Scores must be floats from 0.0 to 1.0.
""".strip()

ANALYSIS_USER_PROMPT_TEMPLATE = """
Question category: {category}
Question difficulty: {difficulty}
Question title: {question_title}
Question description: {question_description}
Has audio attachment: {has_audio}

Candidate answer:
{answer_text}

Return JSON with:
- overall_score: integer 0-100
- scores_by_category: object with structure, relevance, specificity, confidence, completeness
- strengths: 1-3 short strings
- to_improve: 1-3 short strings
- quick_tips: 1-3 short strings
- ideal_answer_example: short improved example answer
- explanation: short explanation of the score
""".strip()
