from datetime import datetime

# Default weights for priority calculation
DEFAULT_WEIGHTS = {
    "importance": 0.5,
    "urgency": 0.3,
    "effort": 0.2,
    "dependencies": 0.4
}

def compute_scores(tasks, weights=DEFAULT_WEIGHTS):
    """
    Accepts a list of task dicts and returns tasks with calculated priority scores.
    """
    scored_tasks = []
    cycles = []

    # Example simple scoring
    for task in tasks:
        score = 0
        importance = task.get("importance", 1)
        estimated_hours = task.get("estimated_hours", 1)
        due_date = task.get("due_date")

        # urgency
        urgency = 0
        if due_date:
            try:
                due = datetime.fromisoformat(due_date).date()
                delta = (due - datetime.today().date()).days
                urgency = 1 / (delta + 1) if delta >= 0 else 2  # past due gets higher urgency
            except:
                urgency = 0
        else:
            urgency = 0

        score = (importance * weights.get("importance", 1) +
                 urgency * weights.get("urgency", 1) +
                 (1 / estimated_hours) * weights.get("effort", 1) +
                 len(task.get("dependencies", [])) * weights.get("dependencies", 1))

        scored_tasks.append({
            "id": task.get("id"),
            "title": task.get("title"),
            "score": round(score, 2),
            "components": {"importance": importance, "urgency": urgency},
            "raw": task
        })

    # sort descending by score
    scored_tasks.sort(key=lambda x: x["score"], reverse=True)

    return {"scored": scored_tasks, "cycles": cycles}
