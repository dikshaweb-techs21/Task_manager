from django.urls import path
from .views import (
    TaskListCreateView, 
    TaskRetrieveUpdateDestroyView,
    TaskAnalyzeAPIView,
    TaskSuggestAPIView,
    index
)

urlpatterns = [
    path('', index, name='index'),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskRetrieveUpdateDestroyView.as_view(), name="task-detail"),
    path("tasks/analyze/", TaskAnalyzeAPIView.as_view(), name="task-analyze"),
    path("tasks/suggest/", TaskSuggestAPIView.as_view(), name="task-suggest"),
]
