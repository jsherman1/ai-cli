def build_revision_prompt(original_prompt: str, previous_draft: str, evaluator_feedback: str) -> str:
    """Formats the prompt to instruct the model to revise its draft based on feedback."""
    return f"""
    You are an expert assistant. You previously wrote a draft for the following prompt:
    Original Prompt: {original_prompt}
    
    Your previous draft: {previous_draft}
    
    An expert reviewer has rejected your draft with the following feedback:
    Reviewer Feedback: {evaluator_feedback}
    
    Please rewrite your draft to entirely satisfy the reviewer's feedback. Output ONLY the new draft without meta-commentary.
    """