# Smart Task Analyzer

A mini-application to intelligently score and prioritize tasks based on importance, urgency, effort, and dependencies.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Smart-Task-Analyzer.git
   cd Smart-Task-Analyzer/backend

2.Create a virtual environment:

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

3.Install dependencies:

pip install -r requirements.txt

4.Run the server:

python manage.py runserver


5.Open in browser:

http://127.0.0.1:8000/



## Algorithm Explanation

The task scoring algorithm calculates a priority score based on four factors:
- **Importance:** Higher importance tasks get higher scores.
- **Urgency:** Tasks closer to their due date are scored higher.
- **Effort:** Tasks with lower estimated hours get a higher score.
- **Dependencies:** Tasks with fewer dependencies are preferred.

Each factor has a weight (default: importance=0.5, urgency=0.3, effort=0.2, dependencies=0.4).  
The final score is computed as a weighted sum. Tasks can also be sorted based on different strategies (fastest, high-impact, deadline) by adjusting these weights. This ensures the user focuses on tasks that maximize efficiency and meet deadlines.



## Design Decisions
- Used Django REST Framework for API simplicity.
- Frontend is plain HTML/CSS/JS for lightweight UI.
- SQLite used for simplicity (no external DB setup).
- Priority scoring separated into `utils/priority.py` for modularity.


## Time Breakdown
- Backend API & Models: 6 hours
- Frontend HTML/CSS/JS: 4 hours
- Scoring algorithm & unit tests: 5 hours
- Debugging & deployment prep: 2 hours

## Bonus Challenges
- Implemented top-3 task suggestion API
- Dependency-aware scoring

## Future Improvements
- Add user authentication
- Add task categories or tags
- Deploy on cloud (Heroku/AWS)
- Enhance UI with frameworks like React

