from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .utils.priority import compute_scores, DEFAULT_WEIGHTS  # use scoring logic

from datetime import date
# List all tasks / Create new task
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Retrieve / Update / Delete single task
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Analyze tasks and calculate priority scores
class TaskAnalyzeAPIView(APIView):
    def post(self, request):
        tasks = request.data.get("tasks", [])
        weights = request.data.get("weights", DEFAULT_WEIGHTS)
        if not tasks:
            return Response({"detail": "Provide 'tasks' as a list"}, status=status.HTTP_400_BAD_REQUEST)

        # Compute priority scores
        scored = compute_scores(tasks, weights=weights)
        return Response({
            "scored": scored["scored"],
            "cycles": scored["cycles"],
            "weights_used": weights
        })


# Suggest top 3 tasks to work on today
# Suggest top 3 tasks to work on today

class TaskSuggestAPIView(APIView):
    def get(self, request):
        n = int(request.query_params.get("n", 3))
        tasks_qs = Task.objects.all()
        tasks = []

        today = date.today()

        for t in tasks_qs:
            try:
                if not t.title or not t.estimated_hours or not t.importance:
                    continue

                estimated_hours = t.estimated_hours or 1
                importance = t.importance or 1
                due_date_iso = t.due_date.isoformat() if t.due_date else None

                urgency = 0
                if due_date_iso:
                    y, m, d = map(int, due_date_iso.split("-"))
                    delta = (date(y, m, d) - today).days
                    urgency = 1 / (delta + 1) if delta >= 0 else 2

                task_dict = {
                    "id": t.id,
                    "title": t.title,
                    "due_date": due_date_iso,
                    "estimated_hours": estimated_hours,
                    "importance": importance,
                    "dependencies": list(t.dependencies.values_list('title', flat=True)),
                    "components": {
                        "importance": importance,
                        "urgency": urgency,
                        "effort": 1 / estimated_hours if estimated_hours > 0 else 0,
                        "dependencies": t.dependencies.count()
                    }
                }
                tasks.append(task_dict)
            except Exception as e:
                # Skip task if any error occurs
                continue

        try:
            scored = compute_scores(tasks)
            top_tasks = scored["scored"][:n]
        except Exception as e:
            # Return empty list if scoring fails
            return Response({"suggestions": []})

        suggestions = []
        for t in top_tasks:
            explanation = []
            due = t["raw"].get("due_date")
            if due:
                try:
                    y, m, d = map(int, due.split("-"))
                    delta = (date(y, m, d) - today).days
                    explanation.append(f"Overdue by {-delta} day(s)" if delta < 0 else f"Due in {delta} day(s)")
                except:
                    explanation.append("Invalid due date")

            explanation.append(f"Importance: {t['components']['importance']}/10")
            explanation.append(f"Estimated Hours: {t['raw'].get('estimated_hours', '?')}")
            suggestions.append({
                "id": t["id"],
                "title": t["title"],
                "score": t["score"],
                "due_date": t["raw"].get("due_date", "N/A"),
                "estimated_hours": t["raw"].get("estimated_hours", "?"),
                "importance": t["raw"].get("importance", "?"),
                "explanation": " | ".join(explanation)
            })

        return Response({"suggestions": suggestions})


from django.shortcuts import render

def index(request):
    return render(request, "tasks/index.html")  # Django will find index.html inside templates/tasks/




