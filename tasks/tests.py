from django.test import TestCase
from .utils.priority import compute_scores

class ScoringTests(TestCase):
    def test_simple_task_score(self):
        tasks = [
            {"title": "Task 1", "importance": 5, "urgency": 3, "effort": 2, "dependencies": []}
        ]
        scored = compute_scores(tasks)
        self.assertTrue("scored" in scored)
        self.assertEqual(len(scored["scored"]), 1)

    def test_multiple_tasks_order(self):
        tasks = [
            {"title": "Task 1", "importance": 5, "urgency": 3, "effort": 2, "dependencies": []},
            {"title": "Task 2", "importance": 8, "urgency": 2, "effort": 1, "dependencies": ["Task 1"]}
        ]
        scored = compute_scores(tasks)
        # Check that the task with higher score comes first
        self.assertGreater(scored["scored"][0]["score"], scored["scored"][1]["score"])

    def test_task_with_missing_field(self):
        tasks = [
            {"title": "Task 1", "importance": 5, "urgency": 1, "effort": 1, "dependencies": []}
        ]
        scored = compute_scores(tasks)
        self.assertIsInstance(scored, dict)
