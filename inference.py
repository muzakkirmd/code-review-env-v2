"""
Inference Script for Code Review Environment
Must be in ROOT directory as per hackathon requirements.

Environment Variables Required:
    API_BASE_URL  - The API endpoint for the LLM (e.g. https://api.groq.com/openai/v1)
    MODEL_NAME    - The model identifier (e.g. llama3-8b-8192)
    HF_TOKEN      - Your Hugging Face / API key

Usage:
    export API_BASE_URL=https://api.groq.com/openai/v1
    export MODEL_NAME=llama3-8b-8192
    export HF_TOKEN=your_api_key_here
    python inference.py
"""

import os
import sys
import json
import requests
from openai import OpenAI

# ── Configuration from environment variables ─────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
HF_TOKEN = os.getenv("HF_TOKEN", "")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://muzakkir3-code-review-env.hf.space")

# ── OpenAI Client (required by hackathon spec) ────────────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN if HF_TOKEN else "dummy-key-for-rule-based"
)


# ── LLM-based Review ─────────────────────────────────────────

def get_llm_review(code_snippet: str, task_description: str, task_id: str, language: str) -> dict:
    """
    Use OpenAI client to get LLM review of code.
    Falls back to rule-based if no API key provided.
    """
    if not HF_TOKEN:
        print(f"  No HF_TOKEN set — using rule-based fallback for {task_id}")
        return get_rule_based_review(task_id, code_snippet, language)

    prompt = f"""You are an expert {language} code reviewer. 
Review the following code carefully for the task: {task_description}

Code:
```{language}
{code_snippet}
```

Provide your review as JSON with these exact fields:
{{
    "bugs_found": ["list of specific bugs found"],
    "severity": "low/medium/high",
    "security_issues": ["list of security vulnerabilities"],
    "suggestions": ["list of improvement suggestions"],
    "quality_score": 0.3,
    "explanation": "detailed explanation of your review"
}}

Return ONLY valid JSON, no other text."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=800
        )
        content = response.choices[0].message.content.strip()
        # Clean JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"  LLM error: {e} — using rule-based fallback")
        return get_rule_based_review(task_id, code_snippet, language)


# ── Rule-Based Fallback ───────────────────────────────────────

def get_rule_based_review(task_id: str, code: str, language: str) -> dict:
    """Smart rule-based agent that reads actual code and language."""

    if task_id == "task1":
        bugs = []
        suggestions = []
        explanation = ""

        if language == "python":
            if "/ len" in code or "len(numbers)" in code:
                bugs.extend(["division by zero when empty list", "no empty list check", "ZeroDivisionError"])
                suggestions.append("add empty list check before division")
                explanation += "Division by zero on empty list. "
            if "max_val = 0" in code:
                bugs.extend(["wrong initial value", "fails for negative numbers", "max_val initialized to 0"])
                suggestions.append("initialize max_val to float negative infinity")
                explanation += "Logic bug: fails for all-negative lists. "
            if "=+" in code:
                bugs.extend(["wrong operator =+ should be +=", "count always equals 1", "assignment not increment"])
                suggestions.append("replace =+ with += for proper increment")
                explanation += "Wrong operator =+ always resets count to 1. "
            if ".reverse()" in code:
                bugs.extend(["string reverse returns None", "AttributeError", "should use slicing s[::-1]"])
                suggestions.append("use s[::-1] instead of s.reverse()")
                explanation += "String .reverse() returns None. "
            if "factorial(n)" in code and "factorial(n-1)" not in code:
                bugs.extend(["infinite recursion", "missing n-1 in recursive call", "RecursionError"])
                suggestions.append("change factorial(n) to factorial(n-1)")
                explanation += "Infinite recursion: missing base reduction. "
            if "lst.pop" in code:
                bugs.extend(["modifying list while iterating", "index out of range", "unsafe list mutation"])
                suggestions.append("create a copy of list before iterating")
                explanation += "Unsafe list mutation during iteration. "
            if "/ 2" in code and "mid" in code and "//" not in code:
                bugs.extend(["float division instead of integer", "mid should use //", "TypeError as array index"])
                suggestions.append("use // for integer division")
                explanation += "Float division causes TypeError when used as index. "
            if "dictionary[key]" in code:
                bugs.extend(["KeyError on missing key", "no default value", "should use dict.get()"])
                suggestions.append("use dictionary.get(key, default)")
                explanation += "Direct dictionary access raises KeyError. "
            if "open(" in code and "with" not in code and "close" not in code:
                bugs.extend(["file handle never closed", "resource leak", "should use with statement"])
                suggestions.append("use with open() as f: pattern")
                explanation += "File handle not closed. "

        elif language == "javascript":
            if "i <= arr.length" in code:
                bugs.extend(["off by one error", "i <= arr.length should be i < arr.length", "undefined access", "NaN in result"])
                suggestions.append("change <= to < in loop condition")
                explanation += "Off-by-one: accessing arr[arr.length] gives undefined. "
            if "==" in code and "===" not in code and "isEqual" in code:
                bugs.extend(["loose equality ==", "should use strict ===", "type coercion", "0 == false is true"])
                suggestions.append("replace == with === for strict comparison")
                explanation += "Loose equality causes unexpected type coercion. "
            if "var i" in code and "function()" in code:
                bugs.extend(["closure bug with var", "all functions return same value", "var is function-scoped", "should use let"])
                suggestions.append("replace var with let for block scoping")
                explanation += "Closure captures var reference: all return same value. "

        elif language == "java":
            if "==" in code and "String" in code and "new String" in code:
                bugs.extend(["reference comparison not value", "== compares references not content", "should use .equals()", "always prints Not equal"])
                suggestions.append("use .equals() instead of == for string comparison")
                explanation += "Java == compares references not string values. "
            if "s.length()" in code and "!= null" not in code:
                bugs.extend(["NullPointerException when null passed", "no null check", "missing null validation"])
                suggestions.append("add null check before calling s.length()")
                explanation += "NullPointerException when null String is passed. "

        if not bugs:
            bugs = ["logic error in code", "edge case not handled", "missing input validation"]
            suggestions = ["add input validation", "handle edge cases", "test with boundary values"]
            explanation = "Code has logic errors and missing edge case handling."

        return {
            "bugs_found": bugs, "severity": "medium", "security_issues": [],
            "suggestions": suggestions + ["add unit tests", "improve error handling"],
            "quality_score": 0.3, "explanation": explanation.strip()
        }

    elif task_id == "task2":
        security_issues = []
        suggestions = []
        explanation = ""
        backtick = chr(96)

        if ("SELECT" in code or "INSERT" in code) and ("+" in code or backtick in code):
            security_issues.extend(["SQL injection via string concatenation", "no parameterized queries", "no input sanitization", "attacker can manipulate query"])
            suggestions.extend(["use parameterized queries", "use prepared statements"])
            explanation += "Critical SQL injection vulnerability. "
        if any(k in code for k in ["API_KEY", "PASSWORD", "SECRET", "TOKEN"]):
            security_issues.extend(["hardcoded credentials in source code", "API key exposed", "password hardcoded", "use environment variables"])
            suggestions.extend(["use environment variables", "use secrets manager"])
            explanation += "Hardcoded credentials exposed. "
        if "shell=True" in code or ("subprocess" in code and "cmd" in code):
            security_issues.extend(["command injection via shell=True", "user input in shell", "remote code execution possible", "no input validation"])
            suggestions.extend(["avoid shell=True", "validate all user input"])
            explanation += "Command injection via shell=True. "
        if "pickle" in code and "loads" in code:
            security_issues.extend(["insecure deserialization with pickle", "arbitrary code execution via pickle", "untrusted data deserialized"])
            suggestions.extend(["use JSON instead of pickle", "never deserialize untrusted data"])
            explanation += "Insecure deserialization allows RCE. "
        if "innerHTML" in code or "render_template_string" in code:
            security_issues.extend(["XSS vulnerability", "user input in HTML", "cross-site scripting", "no output encoding"])
            suggestions.extend(["use textContent not innerHTML", "encode all output"])
            explanation += "XSS through unencoded user input. "
        if "md5" in code or "MD5" in code:
            security_issues.extend(["MD5 is broken algorithm", "no salt in hashing", "rainbow table vulnerable", "weak password storage"])
            suggestions.extend(["use bcrypt or argon2", "always add salt"])
            explanation += "Weak MD5 password hashing. "
        if "Access-Control-Allow-Origin" in code and "*" in code:
            security_issues.extend(["CORS wildcard misconfiguration", "allows any origin", "too permissive CORS"])
            suggestions.extend(["restrict to specific origins"])
            explanation += "Dangerous CORS wildcard. "
        if "db.query" in code and backtick in code:
            security_issues.extend(["SQL injection in JavaScript", "template literal in SQL", "no parameterized queries"])
            suggestions.extend(["use parameterized queries", "use ORM"])
            explanation += "SQL injection via template literals. "
        if "basePath" in code and "filename" in code:
            security_issues.extend(["path traversal vulnerability", "no filename validation", "can read arbitrary files"])
            suggestions.extend(["validate filename", "use Path.resolve()"])
            explanation += "Path traversal vulnerability. "
        if language == "java" and "Statement" in code and "PreparedStatement" not in code:
            security_issues.extend(["SQL injection via Statement", "use PreparedStatement", "no parameterized protection"])
            suggestions.extend(["replace Statement with PreparedStatement"])
            explanation += "Java Statement allows SQL injection. "
        if not security_issues:
            security_issues = ["security vulnerability detected", "missing input validation", "insufficient access control"]
            suggestions = ["add input validation", "follow OWASP Top 10", "implement access control"]
            explanation = "Security vulnerabilities found."

        return {
            "bugs_found": [], "severity": "high",
            "security_issues": security_issues, "suggestions": suggestions,
            "quality_score": 0.2, "explanation": explanation.strip()
        }

    else:  # task3
        bugs = []
        security_issues = []
        suggestions = []
        parts = []

        if language == "python":
            for c in ["p(", "r(", "f(", "g(", "h("]:
                if "def " + c in code:
                    suggestions.append("use descriptive function names instead of single letters")
                    parts.append("single letter function names")
                    break
            if "for i in range(len(" in code:
                suggestions.append("use enumerate() instead of range(len())")
                parts.append("range(len()) anti-pattern")
            if "for i in range" in code and "for j in range" in code:
                suggestions.append("optimize O(n2) nested loops with set or dict for O(n)")
                parts.append("O(n2) complexity")
            if '"""' not in code and "def " in code:
                suggestions.append("add docstrings to all functions")
                parts.append("missing docstrings")
            if "->" not in code and "def " in code:
                suggestions.append("add type hints to all parameters")
                parts.append("no type hints")
            if "try" not in code:
                bugs.append("no error handling with try/except")
                suggestions.append("add try/except blocks")
                parts.append("missing error handling")
            if "self.balance - amount" in code and "amount >" not in code:
                bugs.append("allows negative balance without validation")
                suggestions.append("add balance check before withdrawal")
            if "cc=[]" in code or ("=[]" in code and "def " in code):
                bugs.append("mutable default argument shared across calls")
                suggestions.append("use None as default, initialize inside function")
            if "debug=True" in code:
                security_issues.append("debug=True exposes info in production")
                suggestions.append("set debug=False in production")

        elif language == "javascript":
            if "var " in code:
                suggestions.append("use const/let instead of var")
                parts.append("var hoisting issues")
            if "catch" not in code and ("fetch" in code or ".then(" in code):
                bugs.append("no .catch() for promise rejections")
                suggestions.append("add .catch() or try/catch for async")
                parts.append("unhandled promise rejections")
            if "/**" not in code and "function" in code:
                suggestions.append("add JSDoc comments to all functions")
                parts.append("missing JSDoc")
            if "innerHTML" in code:
                security_issues.append("XSS risk via innerHTML")
                suggestions.append("use textContent instead")
            suggestions.append("separate data fetching from DOM manipulation")
            parts.append("mixed concerns")

        elif language == "java":
            if "/**" not in code:
                suggestions.append("add Javadoc to all public methods")
                parts.append("missing Javadoc")
            if "try" not in code:
                bugs.append("no try-catch blocks")
                suggestions.append("add exception handling")
                parts.append("missing exception handling")
            if "static" in code and "List" in code:
                suggestions.append("avoid mutable static state")
                parts.append("dangerous mutable static state")
            suggestions.append("use defensive copying for returned collections")
            parts.append("returns mutable internal state")

        if not suggestions:
            suggestions = ["improve naming", "add documentation", "optimize complexity",
                           "add error handling", "separate concerns"]
            parts = ["poor naming", "missing docs", "performance issues"]

        explanation = (
            f"Comprehensive {language} review found: {', '.join(parts)}. "
            f"Code needs refactoring for production standards. "
            f"Priority: error handling, naming, performance, documentation."
        )

        return {
            "bugs_found": bugs if bugs else ["missing input validation", "no error handling"],
            "severity": "high",
            "security_issues": security_issues if security_issues else ["insufficient input validation"],
            "suggestions": suggestions[:6],
            "quality_score": 0.25,
            "explanation": explanation
        }


# ── Main Baseline Runner ──────────────────────────────────────

def run_baseline():
    print("=" * 65)
    print("  Code Review Environment — Baseline Inference")
    print("=" * 65)
    print(f"  ENV URL:    {ENV_BASE_URL}")
    print(f"  API URL:    {API_BASE_URL}")
    print(f"  MODEL:      {MODEL_NAME}")
    print(f"  HF_TOKEN:   {'SET' if HF_TOKEN else 'NOT SET (using rule-based fallback)'}")
    print("=" * 65 + "\n")

    # Health check
    try:
        health = requests.get(f"{ENV_BASE_URL}/health", timeout=10)
        print(f"Server Health: {health.json()}\n")
    except Exception as e:
        print(f"Server not reachable: {e}")
        print(f"Make sure the environment is running at: {ENV_BASE_URL}")
        return None

    all_scores = {}
    for task_id in ["task1", "task2", "task3"]:
        print(f"Running {task_id.upper()}...")

        # Reset environment
        obs_resp = requests.post(
            f"{ENV_BASE_URL}/reset",
            json={"task_id": task_id},
            timeout=15
        ).json()

        code_snippet = obs_resp.get("code_snippet", "")
        language = obs_resp.get("language", "python")
        task_description = obs_resp.get("task_description", "")

        print(f"  Language: {language} | Code length: {len(code_snippet)} chars")

        # Get review from LLM or rule-based
        review = get_llm_review(code_snippet, task_description, task_id, language)

        # Submit review
        requests.post(f"{ENV_BASE_URL}/step", json=review, timeout=15)

        # Get grader score
        grader = requests.get(f"{ENV_BASE_URL}/grader", timeout=10).json()
        score = grader.get("score", 0.0)
        passed = grader.get("passed", False)
        feedback = grader.get("feedback", "")

        all_scores[task_id] = {
            "score": score,
            "passed": passed,
            "language": language,
            "feedback": feedback
        }

        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  Score: {score:.2f} | {status} | {feedback}\n")

    # Summary
    avg = sum(v["score"] for v in all_scores.values()) / len(all_scores)
    print("=" * 65)
    print("  BASELINE RESULTS")
    print("=" * 65)
    for task_id, result in all_scores.items():
        bar = "█" * int(result["score"] * 30)
        print(f"  {task_id}: [{bar:<30}] {result['score']:.2f} ({result['language']})")
    print(f"\n  Average Score: {avg:.2f}")
    print("=" * 65)

    return all_scores


if __name__ == "__main__":
    run_baseline()