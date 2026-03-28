# Code Review Environment

> Meta PyTorch OpenEnv Hackathon - Round 1 Submission
> Built by Mohammad Muzakkir Ahmed

A production-ready RL environment where AI agents learn to perform intelligent code reviews.

## Tasks

| Task | Description | Difficulty |
|------|-------------|------------|
| task1 | Syntax & Logic Bug Detection | Easy |
| task2 | Security Vulnerability Detection | Medium |
| task3 | Comprehensive Code Quality Review | Hard |

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## API Endpoints

- `GET /health` - Health check
- `POST /reset` - Start new episode
- `POST /step` - Submit review action
- `GET /state` - Episode state
- `GET /tasks` - List all tasks
- `GET /grader` - Get grader score
- `POST /baseline` - Run baseline agent

## Docker

```bash
docker build -t code-review-env .
docker run -p 7860:7860 code-review-env
```

## Baseline

```bash
python baseline/inference.py
```
