---
title: Code Review Environment
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Code Review Environment
### Meta x PyTorch OpenEnv Hackathon — Round 1 Submission

**Built by Mohammad Muzakkir Ahmed**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-HuggingFace-orange)](https://muzakkir3-code-review-env.hf.space)
[![Docs](https://img.shields.io/badge/API%20Docs-Swagger-green)](https://muzakkir3-code-review-env.hf.space/docs)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-red)](https://github.com/meta-pytorch/OpenEnv)

---

## The Problem Statement

The Meta x PyTorch OpenEnv Hackathon challenged participants to:

> **"Build a complete, real-world OpenEnv environment that an AI agent can learn from through the standard step() / reset() / state() API."**

Key requirements:
- Must simulate a real-world task (NOT games or toys)
- Implement full OpenEnv spec with typed models
- Minimum 3 tasks with graders (Easy to Medium to Hard)
- Meaningful reward function with partial progress signals
- Baseline inference script with reproducible scores
- Deploy to Hugging Face Spaces with working Dockerfile

---

## Why I Chose Code Review

Every software company on earth has the same problem — code review is expensive, slow, and depends on senior engineers who are always busy.

Consider these facts:
- A senior engineer spends 3-5 hours per day reviewing code
- Companies like Google, Amazon, and Meta employ thousands of engineers just for reviews
- Junior developers wait days for feedback on their code
- Bugs that slip past review cost companies millions

The solution? Train AI agents to do code review automatically.

Our environment gives AI agents real Python code snippets and teaches them to find bugs, security vulnerabilities, and quality issues — exactly what a senior engineer does during a pull request review.

This is not a toy problem. This is a skill that has immediate, measurable value in the real world.

---

## What is This Project?

The Code Review Environment is a production-ready Reinforcement Learning environment where AI agents learn to perform intelligent code reviews.

Think of it like this:

Without AI Agent:
- Senior engineer gets PR
- Reads through code for 2-3 hours
- Finds some bugs, misses others
- Junior dev waits 2 days for feedback

With Our AI Environment:
- AI agent receives code snippet
- Analyzes patterns and structures instantly
- Identifies bugs, security issues, quality problems
- Returns structured scored feedback in milliseconds

---

## How It Works

```
AI AGENT
  |
  | obs = env.reset(task_id="task1")   # Get code to review
  | result = env.step(review_action)   # Submit review
  | print(result.reward)               # See score
  |
  v
CODE REVIEW ENVIRONMENT (Running on Hugging Face)
  |
  | 1. Gives agent a real buggy code snippet
  | 2. Agent reviews it and submits findings
  | 3. Grader scores the review (0.0 - 1.0)
  | 4. Agent receives reward and learns
  |
  v
3 TASK GRADERS
  - Task 1: Bug Detection       (Easy)
  - Task 2: Security Detection  (Medium)
  - Task 3: Quality Review      (Hard)
```

---

## The 3 Tasks

### Task 1 — Syntax and Logic Bug Detection (Easy)

The agent receives Python code with obvious bugs and must identify them.

Example code given to agent:
```python
def find_max(lst):
    max_val = 0          # BUG: fails for all-negative inputs
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val

print(find_max([-5, -3, -1]))  # Returns 0, should return -1
```

What the agent must find: The function returns wrong results for negative numbers because max_val is initialized to 0 instead of the first element.

Scoring: 0.0 to 1.0 based on bugs correctly identified.

---

### Task 2 — Security Vulnerability Detection (Medium)

The agent must identify real security vulnerabilities that could compromise systems.

Example code given to agent:
```python
import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # CRITICAL: SQL Injection vulnerability!
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
```

What the agent must find: SQL injection vulnerability, no parameterized queries, no input sanitization.

Scoring: 0.0 to 1.0 based on vulnerabilities correctly identified.

---

### Task 3 — Comprehensive Code Quality Review (Hard)

The agent must perform a full professional code review covering multiple dimensions.

Example code given to agent:
```python
def p(d):           # Bad naming - what does p or d mean?
    r = []
    for i in range(len(d)):      # O(n2) - terrible performance
        for j in range(len(d)):
            if i != j:
                if d[i] == d[j]:
                    if d[i] not in r:
                        r.append(d[i])
    return r
```

What the agent must find:
- Naming: p and d are meaningless variable names
- Performance: O(n2) complexity when a set would be O(n)
- Documentation: No docstring, no type hints, no comments
- Design: Overcomplicated, can be done in one line with set

Scoring: 0.0 to 1.0 across naming, performance, documentation, design, and error handling.

---

## Reward Function

The reward is NOT binary — it provides partial progress signals:

| Component | Weight | Description |
|---|---|---|
| Grader score | 70% | Based on issues correctly identified |
| Explanation depth | 10% | Bonus for detailed explanations |
| Suggestion count | 10% | Bonus for 3+ actionable suggestions |
| Severity accuracy | 10% | Bonus for correct severity level |
| Empty review | -20% | Penalty for submitting nothing |

An agent that finds half the bugs still gets rewarded. It does not need to be perfect to learn.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /reset | POST | Start new episode, get code to review |
| /step | POST | Submit review action, get reward |
| /state | GET | Get current episode metadata |
| /tasks | GET | List all tasks with action schemas |
| /grader | GET | Get detailed grader score |
| /baseline | POST | Run baseline agent on all 3 tasks |

---

## Quick Start

### Try it in browser:
```
https://muzakkir3-code-review-env.hf.space/docs
```

### Use it in Python:
```python
import requests

BASE = "https://muzakkir3-code-review-env.hf.space"

# Get a code snippet to review
obs = requests.post(f"{BASE}/reset", json={"task_id": "task1"}).json()
print(obs["code_snippet"])

# Submit your review
result = requests.post(f"{BASE}/step", json={
    "bugs_found": ["max_val initialized to 0 fails for negative numbers"],
    "severity": "medium",
    "suggestions": ["initialize max_val to float('-inf')"],
    "quality_score": 0.3,
    "explanation": "Function returns wrong results for all-negative lists."
}).json()

print(f"Reward: {result['reward']}")
print(f"Feedback: {result['feedback']}")
```

### Run with Docker:
```bash
docker build -t code-review-env .
docker run -p 7860:7860 code-review-env
```

---

## Project Structure

```
code-review-env/
|-- main.py                    Entry point
|-- Dockerfile                 Container definition
|-- requirements.txt           Dependencies
|-- openenv.yaml               OpenEnv metadata
|-- src/
|   |-- code_review_env/
|       |-- models.py          Typed Pydantic models
|       |-- server/
|           |-- environment.py Core game logic
|-- tasks/
|   |-- task1_syntax.py        Easy: Bug detection + grader
|   |-- task2_security.py      Medium: Security + grader
|   |-- task3_quality.py       Hard: Quality review + grader
|-- baseline/
|   |-- inference.py           Baseline agent script
|-- tests/
    |-- test_environment.py    Test suite
```

---

## Baseline Scores

| Task | Score | Status |
|---|---|---|
| Task 1 - Bug Detection (Easy) | 0.67 | Passed |
| Task 2 - Security Detection (Medium) | 0.70 | Passed |
| Task 3 - Quality Review (Hard) | 0.55 | Passed |
| Average | 0.64 | All Passed |

---

## Pros and Cons

### Advantages
- Solves a real problem every tech company faces daily
- Clear deterministic scoring from 0.0 to 1.0
- Three difficulty levels for curriculum learning
- Works with any LLM (GPT, Claude, Llama, Gemini)
- Deployed live on Hugging Face — anyone can use it now
- Full OpenEnv spec compliance
- Docker containerized for reproducibility

### Current Limitations
- Currently covers Python only
- Grader uses keyword matching not deep semantic analysis
- Limited number of code snippets
- Single-turn episodes only

### Future Improvements
- Add 50+ code snippets per task
- Support JavaScript, Java, Go, Rust
- Integrate real code execution and unit tests
- Multi-turn conversation for iterative review
- GitHub Pull Request integration

---

## Why This Stands Out

| Typical Environment | Code Review Environment |
|---|---|
| Game (catch, chess, maze) | Real software engineering task |
| Abstract reward | Measurable business value |
| Toy problem | Industry-scale problem |
| No practical use | Companies can use this today |
| Agent learns game rules | Agent learns engineering skills |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Core language |
| FastAPI | Web server framework |
| Pydantic | Type-safe data models |
| Docker | Containerization |
| Hugging Face Spaces | Cloud deployment |
| OpenEnv | RL environment framework |

---

## Live Links

- API Docs: https://muzakkir3-code-review-env.hf.space/docs
- Health Check: https://muzakkir3-code-review-env.hf.space/health
- All Tasks: https://muzakkir3-code-review-env.hf.space/tasks
- HF Space: https://huggingface.co/spaces/Muzakkir3/code-review-env
- GitHub: https://github.com/muzakkirmd/code-review-env-v2

---

## About

Built for the Meta x PyTorch OpenEnv Hackathon organized by Scaler School of Technology.

Developer: Mohammad Muzakkir Ahmed
GitHub: @muzakkirmd

---

## License

MIT License — Mohammad Muzakkir Ahmed, 2026
