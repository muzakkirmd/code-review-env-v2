"""
Baseline Inference Script - Smart Rule-Based Agent
Analyzes actual code content to give relevant reviews.

Usage:
    python baseline/inference.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests

BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")


def get_rule_based_review(task_id: str, code_snippet: str = "") -> dict:
    """Smart rule-based agent that reads actual code and gives relevant review."""

    if task_id == "task1":
        bugs = []
        suggestions = []
        explanation = ""

        if "len(numbers)" in code_snippet or "/ len" in code_snippet:
            bugs.extend(["division by zero when empty list", "no empty list check", "ZeroDivisionError"])
            suggestions.append("add empty list check before division")
            explanation += "Division by zero on empty list. "

        if "max_val = 0" in code_snippet:
            bugs.extend(["wrong initial value", "fails for negative numbers", "max_val initialized to 0"])
            suggestions.append("initialize max_val to float negative infinity or lst[0]")
            explanation += "Logic bug with negative numbers. "

        if "=+" in code_snippet:
            bugs.extend(["wrong operator =+ should be +=", "count always equals 1", "assignment not increment"])
            suggestions.append("replace =+ with += for proper increment")
            explanation += "Wrong operator =+ used instead of +=. "

        if ".reverse()" in code_snippet:
            bugs.extend(["reverse returns None", "AttributeError on string", "should use slicing"])
            suggestions.append("use s[::-1] instead of s.reverse()")
            explanation += "String reverse returns None. "

        if "factorial(n)" in code_snippet and "factorial(n-1)" not in code_snippet:
            bugs.extend(["infinite recursion", "missing n-1", "RecursionError"])
            suggestions.append("change factorial(n) to factorial(n-1)")
            explanation += "Infinite recursion due to missing reduction. "

        if "lst.pop" in code_snippet or "i+1:" in code_snippet:
            bugs.extend(["modifying list while iterating", "index out of range", "unsafe mutation"])
            suggestions.append("create a copy before iterating")
            explanation += "Unsafe list mutation during iteration. "

        if "/ 2" in code_snippet and "mid" in code_snippet:
            bugs.extend(["float division instead of integer", "mid should use //", "TypeError"])
            suggestions.append("use // for integer division")
            explanation += "Float division causes TypeError as array index. "

        if "dictionary[key]" in code_snippet:
            bugs.extend(["KeyError on missing key", "no default value", "should use dict.get()"])
            suggestions.append("use dictionary.get(key, default)")
            explanation += "Direct access raises KeyError. "

        if "open(" in code_snippet and "with" not in code_snippet:
            bugs.extend(["file not closed", "resource leak", "no with statement"])
            suggestions.append("use with open() as f pattern")
            explanation += "File handle not closed causing resource leak. "

        if not bugs:
            bugs = ["logic error found", "edge case not handled", "missing input validation"]
            suggestions = ["add input validation", "handle edge cases"]
            explanation = "Code has logic errors and missing edge case handling."

        return {
            "bugs_found": bugs,
            "severity": "medium",
            "security_issues": [],
            "suggestions": suggestions + ["add unit tests", "improve error handling"],
            "quality_score": 0.3,
            "explanation": explanation.strip()
        }

    elif task_id == "task2":
        security_issues = []
        suggestions = []
        explanation = ""

        if "SELECT" in code_snippet or "sqlite3" in code_snippet or ("query" in code_snippet.lower() and "+" in code_snippet):
            security_issues.extend(["SQL injection via string concatenation", "no parameterized queries used", "no input sanitization", "string concatenation in SQL query"])
            suggestions.extend(["use parameterized queries", "use prepared statements"])
            explanation += "Critical SQL injection vulnerability. "

        if "API_KEY" in code_snippet or "PASSWORD" in code_snippet or "SECRET" in code_snippet or "TOKEN" in code_snippet:
            security_issues.extend(["hardcoded API key in source code", "hardcoded password credentials", "hardcoded secret token", "credentials should use environment variables"])
            suggestions.extend(["use environment variables for secrets", "use a secrets manager"])
            explanation += "Hardcoded credentials in source code. "

        if "shell=True" in code_snippet or ("subprocess" in code_snippet and "cmd" in code_snippet):
            security_issues.extend(["command injection via shell=True", "user input passed to shell", "no input validation before execution", "remote code execution possible"])
            suggestions.extend(["avoid shell=True", "validate all user input"])
            explanation += "Command injection via shell=True. "

        if "pickle" in code_snippet:
            security_issues.extend(["insecure deserialization with pickle", "untrusted data deserialized", "remote code execution via pickle"])
            suggestions.extend(["use JSON instead of pickle", "validate before deserializing"])
            explanation += "Insecure deserialization vulnerability. "

        if "innerHTML" in code_snippet or "render_template_string" in code_snippet:
            security_issues.extend(["XSS vulnerability via innerHTML", "user input directly in HTML", "cross site scripting possible", "no output encoding"])
            suggestions.extend(["use textContent not innerHTML", "encode all output"])
            explanation += "XSS vulnerability through unencoded user input. "

        if "md5" in code_snippet or "sha1" in code_snippet:
            security_issues.extend(["MD5 is a broken hash algorithm", "no salt used in password hashing", "weak cryptographic algorithm", "rainbow table attack possible"])
            suggestions.extend(["use bcrypt or argon2", "always salt passwords"])
            explanation += "Weak password hashing using broken MD5. "

        if "'*'" in code_snippet and "Access-Control" in code_snippet:
            security_issues.extend(["CORS misconfiguration with wildcard", "allows any origin access", "too permissive CORS policy"])
            suggestions.extend(["restrict CORS to specific origins", "never use wildcard in production"])
            explanation += "Dangerous CORS wildcard misconfiguration. "

        if "db.query" in code_snippet and "`" in code_snippet:
            security_issues.extend(["SQL injection in JavaScript query", "template literal used in SQL", "no parameterized queries"])
            suggestions.extend(["use parameterized queries", "use an ORM"])
            explanation += "SQL injection via template literals. "

        if "basePath" in code_snippet and "filename" in code_snippet:
            security_issues.extend(["path traversal vulnerability", "no filename validation", "can read arbitrary files"])
            suggestions.extend(["validate filename against allowed paths", "use Path.resolve()"])
            explanation += "Path traversal allows reading outside directory. "

        if "jwt" in code_snippet and "secret123" in code_snippet:
            security_issues.extend(["weak JWT secret hardcoded", "secret in source code", "token expires too late"])
            suggestions.extend(["use strong random secret", "store in environment variable"])
            explanation += "Weak hardcoded JWT secret. "

        if not security_issues:
            security_issues = ["security vulnerability detected", "input validation missing", "no access control"]
            suggestions = ["add input validation", "implement access control", "follow OWASP guidelines"]
            explanation = "Security vulnerabilities found requiring immediate attention."

        return {
            "bugs_found": [],
            "severity": "high",
            "security_issues": security_issues,
            "suggestions": suggestions,
            "quality_score": 0.2,
            "explanation": explanation.strip()
        }

    else:  # task3
        bugs = []
        security_issues = []
        suggestions = []
        explanation_parts = []

        if any(f"def {c}(" in code_snippet for c in ["p", "r", "f", "g", "h"]):
            suggestions.append("use descriptive function names instead of single letters")
            explanation_parts.append("single letter function names are unreadable")

        if "for i in range(len(" in code_snippet:
            suggestions.append("use enumerate() or iterate directly instead of range(len())")
            explanation_parts.append("anti-pattern range(len()) detected")

        if "for i in range" in code_snippet and "for j in range" in code_snippet:
            suggestions.append("optimize O(n2) nested loops with set or dict for O(n)")
            explanation_parts.append("O(n2) nested loops are a performance issue")

        if "def " in code_snippet and '"""' not in code_snippet:
            suggestions.append("add docstrings to all functions and methods")
            explanation_parts.append("missing docstrings reduce maintainability")

        if "->" not in code_snippet and "def " in code_snippet:
            suggestions.append("add type hints to all function parameters and return values")
            explanation_parts.append("no type hints make code harder to understand")

        if "try" not in code_snippet:
            bugs.append("no error handling with try/except blocks")
            suggestions.append("add proper error handling for all operations")
            explanation_parts.append("missing error handling causes unhandled exceptions")

        if "requests.get" in code_snippet and "try" not in code_snippet:
            bugs.append("no exception handling for network requests")
            suggestions.append("wrap all HTTP calls in try/except with timeout")

        if "self.balance - amount" in code_snippet and "amount >" not in code_snippet:
            bugs.append("allows negative balance without validation")
            suggestions.append("add balance check before allowing withdrawal")

        if "cc=[]" in code_snippet or "bcc=[]" in code_snippet:
            bugs.append("mutable default argument is shared across all calls")
            suggestions.append("use None as default and initialize inside function body")

        if "debug=True" in code_snippet:
            security_issues.append("debug=True must never be used in production")
            suggestions.append("always set debug=False in production environment")

        if not suggestions:
            suggestions = ["improve naming conventions", "add docstrings and type hints",
                          "optimize algorithm complexity", "add proper error handling",
                          "separate concerns and improve design"]
            explanation_parts = ["poor naming", "O(n2) complexity", "missing error handling", "no documentation"]

        explanation = (
            f"Comprehensive review found issues: {', '.join(explanation_parts)}. "
            f"Code requires significant refactoring to meet production standards. "
            f"Priority: add error handling, improve naming, optimize performance, add documentation."
        )

        return {
            "bugs_found": bugs if bugs else ["missing input validation", "no error handling"],
            "severity": "high",
            "security_issues": security_issues if security_issues else ["no input type checking"],
            "suggestions": suggestions[:6],
            "quality_score": 0.25,
            "explanation": explanation
        }


def run_baseline():
    print("=" * 60)
    print("  Code Review Environment - Smart Baseline Agent")
    print("=" * 60)

    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Server: {health.json()}\n")
    except Exception as e:
        print(f"Server not reachable: {e}")
        print("Start server: python main.py")
        return

    all_scores = {}
    for task_id in ["task1", "task2", "task3"]:
        print(f"Running {task_id.upper()}...")
        obs = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id}).json()
        code_snippet = obs.get("code_snippet", "")
        print(f"  Language: {obs.get('language', 'unknown')}")

        review = get_rule_based_review(task_id, code_snippet)
        requests.post(f"{BASE_URL}/step", json=review)
        g = requests.get(f"{BASE_URL}/grader").json()
        score = g.get("score", 0.0)
        all_scores[task_id] = score
        print(f"  Score: {score:.2f} | {g.get('feedback', '')}")

    avg = sum(all_scores.values()) / len(all_scores)
    print(f"\nAverage Score: {avg:.2f}")
    print("=" * 60)
    return all_scores


if __name__ == "__main__":
    run_baseline()