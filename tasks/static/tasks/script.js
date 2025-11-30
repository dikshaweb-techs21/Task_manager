async function addTask(event) {
    event.preventDefault();

    const task = {
        title: document.getElementById('title').value.trim(),
        due_date: document.getElementById('due_date').value,
        estimated_hours: parseFloat(document.getElementById('estimated_hours').value),
        importance: parseInt(document.getElementById('importance').value),
        dependencies: Array.from(document.getElementById('dependencies').selectedOptions).map(opt => opt.value)
    };

    if (!task.title || isNaN(task.estimated_hours) || isNaN(task.importance)) {
        alert('Please fill all required fields correctly.');
        return;
    }

    const response = await fetch('/tasks/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task)
    });

    if (response.ok) {
        alert('Task added successfully!');
        document.getElementById('task-form').reset();

        // Reload dependencies after adding a new task
        const allTasks = await (await fetch('/tasks/')).json();
        updateDependenciesDropdown(allTasks);

        // Optionally refresh task suggestions
        await getSuggestions();
    } else {
        const data = await response.json();
        alert('Error: ' + JSON.stringify(data));
    }
}

async function saveBulkTasks(tasks) {
    for (let task of tasks) {
        if (!task.title || !task.estimated_hours || !task.importance) {
            console.warn("Skipped invalid task:", task);
            continue;
        }
        await fetch('/tasks/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(task)
        });
    }
}

async function analyzeTasks() {
    const bulkText = document.getElementById('bulk-tasks').value;
    let tasks = [];
    try {
        tasks = JSON.parse(bulkText);
    } catch {
        alert('Invalid JSON!');
        return;
    }

    tasks = tasks.filter(t => t.title && !isNaN(t.estimated_hours) && !isNaN(t.importance));
    if (tasks.length === 0) {
        alert('No valid tasks to analyze.');
        return;
    }

    await saveBulkTasks(tasks);
    document.getElementById('bulk-tasks').value = '';

    const strategy = document.getElementById('sorting-strategy').value;
    const response = await fetch('/tasks/analyze/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tasks, weights: getWeights(strategy) })
    });

    if (response.ok) {
        const data = await response.json();
        displayTasks(data.scored);
    } else {
        alert('Error analyzing tasks');
    }
}

async function getSuggestions() {
    try {
        const response = await fetch('/tasks/suggest/?n=3');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        displayTasks(data.suggestions);
    } catch (err) {
        console.error("Failed to get suggestions:", err);
        alert("Could not load suggestions. Check server logs.");
    }
}

function displayTasks(tasks) {
    const container = document.getElementById('task-list');
    container.innerHTML = '';

    tasks.forEach(t => {
        const due = t.due_date || 'N/A';
        const hours = !isNaN(t.estimated_hours) ? t.estimated_hours : '?';
        const importance = !isNaN(t.importance) ? t.importance : '?';
        const score = t.score !== undefined ? t.score.toFixed(2) : '?';

        const div = document.createElement('div');
        div.className = 'task-card ' + getPriorityColor(t.score || 0);
        div.innerHTML = `
            <h3>${t.title}</h3>
            <p>Due: ${due}</p>
            <p>Hours: ${hours}</p>
            <p>Importance: ${importance}</p>
            <p>Score: ${score}</p>
            <p>${t.explanation || ''}</p>
        `;
        container.appendChild(div);
    });
}

function getPriorityColor(score) {
    if(score >= 8) return 'high';
    if(score >= 5) return 'medium';
    return 'low';
}

function getWeights(strategy) {
    switch(strategy) {
        case 'fastest': return { importance: 0.2, urgency: 0.3, effort: 0.5, dependencies: 0.4 };
        case 'high-impact': return { importance: 1, urgency: 0.2, effort: 0.1, dependencies: 0.3 };
        case 'deadline': return { importance: 0.3, urgency: 1, effort: 0.2, dependencies: 0.4 };
        default: return { importance: 0.5, urgency: 0.3, effort: 0.2, dependencies: 0.4 };
    }
}

// Fix duplicates: clear first, then populate
function updateDependenciesDropdown(tasks) {
    const dropdown = document.getElementById('dependencies');
    dropdown.innerHTML = '';  // Clear existing options

    const seen = new Set();
    tasks.forEach(task => {
        if (!seen.has(task.id)) {
            const option = document.createElement('option');
            option.value = task.id;
            option.textContent = task.title;
            dropdown.appendChild(option);
            seen.add(task.id);
        }
    });
}

// Initial load
window.onload = async () => {
    const allTasks = await (await fetch('/tasks/')).json();
    updateDependenciesDropdown(allTasks);
    await getSuggestions();
};

document.getElementById('task-form').addEventListener('submit', addTask);
document.getElementById('analyze-btn').addEventListener('click', analyzeTasks);
