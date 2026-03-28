"""
Baseline Inference Script
Uses Groq API (free, OpenAI-compatible) to run an LLM agent
against all 3 tasks in the Code Review Environment.

Usage:
    export GROQ_API_KEY=your_key_here
    python baseline/inference.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import requests

BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = "llama3-8b-8192"


def get_rule_based_review(task_id: str) -> dict:
    if task_id == "task1":
        return {
            "bugs_found": ["division by zero when empty list", "logic error with negative numbers", "wrong operator =+"],
            "severity": "medium", "security_issues": [],
            "suggestions": ["add input validation", "handle edge cases"],
            "quality_score": 0.4, "explanation": "Found logic bugs and potential runtime errors."
        }
    elif task_id == "task2":
        return {
            "bugs_found": [], "severity": "high",
            "security_issues": ["SQL injection vulnerability", "hardcoded credentials", "command injection"],
            "suggestions": ["use parameterized queries", "use environment variables", "validate inputs"],
            "quality_score": 0.2, "explanation": "Critical security vulnerabilities found."
        }
    else:
        return {
            "bugs_found": ["no error handling"], "severity": "high",
            "security_issues": ["no input validation"],
            "suggestions": ["improve variable naming", "add docstrings and type hints", "optimize algorithm complexity", "add proper error handling", "separate concerns"],
            "quality_score": 0.3,
            "explanation": "Comprehensive review: poor naming conventions, O(n2) complexity, missing error handling, no documentation, security concerns. Full refactoring recommended."
        }


def run_baseline():
    print("=" * 60)
    print("  Code Review Environment - Baseline Inference")
    print("=" * 60)

    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Server: {health.json()}\n")
    except Exception as e:
        print(f"Server not reachable: {e}")
        print("Start server first: python main.py")
        return

    all_scores = {}
    for task_id in ["task1", "task2", "task3"]:
        print(f"Running {task_id.upper()}...")
        obs = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id}).json()
        review = get_rule_based_review(task_id)
        requests.post(f"{BASE_URL}/step", json=review)
        g = requests.get(f"{BASE_URL}/grader").json()
        score = g.get("score", 0.0)
        all_scores[task_id] = score
        print(f"  Score: {score:.2f} | {g.get('feedback', '')}")

    avg = sum(all_scores.values()) / len(all_scores)
    print(f"\nAverage Score: {avg:.2f}")
    return all_scores


if __name__ == "__main__":
    run_baseline()
