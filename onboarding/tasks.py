from celery import shared_task
from time import sleep
from .models import AIResponse, IdeaDraft

@shared_task(bind=True)
def generate_idea_task(self, ai_response_id):
    ai_response = AIResponse.objects.get(id=ai_response_id)
    problem = ai_response.input_payload.get("problem_text", "")
    sleep(3) # Simulating AI process
    generated_idea = f"This is a generated startup idea for problem: {problem}"
    ai_response.output_text = generated_idea
    ai_response.status = "success"
    ai_response.save()
    # Link the idea to corresponding IdeaDraft
    try:
        idea_draft = IdeaDraft.objects.get(ai_response=ai_response)
        idea_draft.generated_idea = generated_idea
        idea_draft.save()
    except IdeaDraft.DoesNotExist:
        pass
    return generated_idea
