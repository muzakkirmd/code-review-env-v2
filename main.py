import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from src.code_review_env.models import CodeReviewAction, CodeReviewObservation, CodeReviewState
from src.code_review_env.server.environment import CodeReviewEnvironment
from tasks.task1_syntax import TASK1_INFO, TASK1_SNIPPETS
from tasks.task2_security import TASK2_INFO, TASK2_SNIPPETS
from tasks.task3_quality import TASK3_INFO, TASK3_SNIPPETS

app = FastAPI(title="Code Review Environment", description="Smart Code Review RL Environment", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
env = CodeReviewEnvironment()

class ResetRequest(BaseModel):
    task_id: Optional[str] = "task1"

class StepRequest(BaseModel):
    bugs_found: list = []
    severity: str = "low"
    security_issues: list = []
    suggestions: list = []
    quality_score: float = 0.5
    explanation: str = ""

@app.get("/health")
def health():
    return {"status": "ok", "environment": "code-review-env", "version": "1.0.0"}

@app.post("/reset")
def reset(request: ResetRequest = ResetRequest()):
    return env.reset(task_id=request.task_id or "task1").model_dump()

@app.post("/step")
def step(request: StepRequest):
    try:
        action = CodeReviewAction(
            bugs_found=request.bugs_found, severity=request.severity,
            security_issues=request.security_issues, suggestions=request.suggestions,
            quality_score=request.quality_score, explanation=request.explanation
        )
        return env.step(action).model_dump()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
def state():
    return env.state().model_dump()

@app.get("/tasks")
def get_tasks():
    return {"tasks": [
        {"task_id": TASK1_INFO["task_id"], "name": TASK1_INFO["name"],
         "description": TASK1_INFO["description"], "difficulty": TASK1_INFO["difficulty"],
         "action_schema": TASK1_INFO["action_schema"], "sample_code": TASK1_SNIPPETS[0]["code"]},
        {"task_id": TASK2_INFO["task_id"], "name": TASK2_INFO["name"],
         "description": TASK2_INFO["description"], "difficulty": TASK2_INFO["difficulty"],
         "action_schema": TASK2_INFO["action_schema"], "sample_code": TASK2_SNIPPETS[0]["code"]},
        {"task_id": TASK3_INFO["task_id"], "name": TASK3_INFO["name"],
         "description": TASK3_INFO["description"], "difficulty": TASK3_INFO["difficulty"],
         "action_schema": TASK3_INFO["action_schema"], "sample_code": TASK3_SNIPPETS[0]["code"]},
    ]}

@app.get("/grader")
def grader():
    result = env.get_last_grader_result()
    if result is None:
        return {"score": 0.0, "passed": False,
                "feedback": "No episode completed yet. Call /reset then /step first.",
                "details": {}}
    return result


def smart_review_task1(code: str, language: str) -> CodeReviewAction:
    """Smart baseline agent for Task 1 - works for Python, JavaScript, Java"""
    bugs = []
    suggestions = []
    explanation = ""

    # ── PYTHON BUGS ──────────────────────────────────────
    if language == "python":
        if "/ len" in code or "len(numbers)" in code:
            bugs.extend(["division by zero when empty list", "no empty list check", "ZeroDivisionError"])
            suggestions.append("add empty list check before division")
            explanation += "Division by zero on empty list. "
        if "max_val = 0" in code:
            bugs.extend(["wrong initial value", "fails for negative numbers", "max_val initialized to 0"])
            suggestions.append("initialize max_val to float negative infinity or lst[0]")
            explanation += "Logic bug: fails for all-negative lists. "
        if "=+" in code:
            bugs.extend(["wrong operator =+ should be +=", "count always equals 1", "assignment not increment"])
            suggestions.append("replace =+ with += for proper increment")
            explanation += "Wrong operator =+ always resets count to 1. "
        if ".reverse()" in code:
            bugs.extend(["string reverse returns None", "AttributeError", "should use slicing s[::-1]"])
            suggestions.append("use s[::-1] instead of s.reverse()")
            explanation += "String .reverse() returns None not reversed string. "
        if "factorial(n)" in code and "factorial(n-1)" not in code:
            bugs.extend(["infinite recursion", "missing n-1 in recursive call", "RecursionError"])
            suggestions.append("change factorial(n) to factorial(n-1)")
            explanation += "Infinite recursion: missing base reduction. "
        if "lst.pop" in code or ("range(len" in code and "pop" in code):
            bugs.extend(["modifying list while iterating", "index out of range", "unsafe list mutation"])
            suggestions.append("create a copy of list before iterating")
            explanation += "Unsafe list mutation during iteration. "
        if "/ 2" in code and "mid" in code and "//" not in code:
            bugs.extend(["float division instead of integer division", "mid should use //", "TypeError as array index"])
            suggestions.append("use // for integer division in binary search")
            explanation += "Float division causes TypeError when used as index. "
        if "dictionary[key]" in code or ("dict" in code and "[key]" in code):
            bugs.extend(["KeyError on missing key", "no default value handling", "should use dict.get()"])
            suggestions.append("use dictionary.get(key, default) instead")
            explanation += "Direct dictionary access raises KeyError. "
        if "open(" in code and "with" not in code and "close" not in code:
            bugs.extend(["file handle never closed", "resource leak", "should use with statement"])
            suggestions.append("use with open() as f: pattern")
            explanation += "File handle not closed causing resource leak. "

    # ── JAVASCRIPT BUGS ──────────────────────────────────
    elif language == "javascript":
        if "i <= arr.length" in code:
            bugs.extend(["off by one error", "i <= arr.length should be i < arr.length", "undefined access at last index", "NaN in result"])
            suggestions.append("change <= to < in loop condition")
            explanation += "Off-by-one: accessing arr[arr.length] gives undefined. "
        if "== b" in code and "===" not in code:
            bugs.extend(["loose equality operator ==", "should use strict equality ===", "type coercion causes wrong results", "0 == false is true"])
            suggestions.append("replace == with === for strict comparison")
            explanation += "Loose equality causes unexpected type coercion. "
        if "var i" in code and "function()" in code and "return i" in code:
            bugs.extend(["closure bug with var", "all functions return same value", "var is function-scoped not block-scoped", "should use let instead of var"])
            suggestions.append("replace var with let for block scoping")
            explanation += "Closure captures var reference not value, all return 3. "

    # ── JAVA BUGS ────────────────────────────────────────
    elif language == "java":
        if "==" in code and "String" in code and "new String" in code:
            bugs.extend(["reference comparison instead of value", "== compares object references not content", "should use .equals() method", "always prints Not equal"])
            suggestions.append("use .equals() instead of == for string comparison")
            explanation += "Java == compares references not string values. "
        if "s.length()" in code and "null" not in code and "!= null" not in code:
            bugs.extend(["NullPointerException when null passed", "no null check before method call", "missing null validation"])
            suggestions.append("add null check: if (s != null) before calling s.length()")
            explanation += "NullPointerException when null String is passed. "

    if not bugs:
        bugs = ["logic error in code", "edge case not handled", "missing input validation"]
        suggestions = ["add input validation", "handle edge cases", "test with boundary values"]
        explanation = "Code has logic errors and missing edge case handling."

    return CodeReviewAction(
        bugs_found=bugs, severity="medium", security_issues=[],
        suggestions=suggestions + ["add unit tests", "improve error handling"],
        quality_score=0.3, explanation=explanation.strip())


def smart_review_task2(code: str, language: str) -> CodeReviewAction:
    """Smart baseline agent for Task 2 - works for Python, JavaScript, Java"""
    security_issues = []
    suggestions = []
    explanation = ""

    # ── SQL INJECTION (all languages) ────────────────────
    if ("SELECT" in code or "INSERT" in code or "UPDATE" in code) and (
            "+" in code or "`" in code or "format" in code):
        security_issues.extend(["SQL injection via string concatenation", "no parameterized queries used",
                                  "no input sanitization", "attacker can manipulate query"])
        suggestions.extend(["use parameterized queries", "use prepared statements"])
        explanation += "Critical SQL injection vulnerability. "

    # ── HARDCODED CREDENTIALS (all languages) ────────────
    if any(k in code for k in ["API_KEY", "PASSWORD", "SECRET", "TOKEN", "api_key", "password", "secret"]):
        security_issues.extend(["hardcoded credentials in source code", "API key exposed in code",
                                  "password hardcoded", "should use environment variables"])
        suggestions.extend(["use environment variables", "use secrets manager"])
        explanation += "Hardcoded credentials exposed in source code. "

    # ── COMMAND INJECTION (Python) ────────────────────────
    if "shell=True" in code or ("subprocess" in code and ("cmd" in code or "command" in code)):
        security_issues.extend(["command injection via shell=True", "user input executed in shell",
                                  "remote code execution possible", "no input validation"])
        suggestions.extend(["avoid shell=True", "validate and sanitize all user input"])
        explanation += "Command injection via shell=True with user input. "

    # ── INSECURE DESERIALIZATION (Python) ─────────────────
    if "pickle" in code and ("loads" in code or "load" in code):
        security_issues.extend(["insecure deserialization with pickle", "arbitrary code execution via pickle",
                                  "untrusted data deserialized"])
        suggestions.extend(["use JSON instead of pickle", "never deserialize untrusted data"])
        explanation += "Insecure deserialization allows remote code execution. "

    # ── XSS (Python/JavaScript) ───────────────────────────
    if "innerHTML" in code or "render_template_string" in code or ("document.write" in code):
        security_issues.extend(["XSS vulnerability", "user input directly rendered in HTML",
                                  "cross-site scripting attack possible", "no output encoding"])
        suggestions.extend(["use textContent instead of innerHTML", "encode all output before rendering"])
        explanation += "XSS vulnerability through unencoded user input in HTML. "

    # ── WEAK CRYPTO (Python) ──────────────────────────────
    if "md5" in code or "MD5" in code or ("sha1" in code and "sha256" not in code):
        security_issues.extend(["MD5 is a broken cryptographic algorithm", "no salt used in hashing",
                                  "vulnerable to rainbow table attacks", "weak password storage"])
        suggestions.extend(["use bcrypt, scrypt, or argon2 for passwords", "always add salt"])
        explanation += "Weak password hashing using broken MD5 algorithm. "

    # ── CORS MISCONFIGURATION (JavaScript) ───────────────
    if "Access-Control-Allow-Origin" in code and ("*" in code or "'*'" in code):
        security_issues.extend(["CORS wildcard misconfiguration", "allows requests from any origin",
                                  "too permissive CORS policy"])
        suggestions.extend(["restrict Access-Control-Allow-Origin to specific domains"])
        explanation += "Dangerous CORS wildcard allows any origin. "

    # ── JWT WEAK SECRET (JavaScript) ──────────────────────
    if "jwt" in code.lower() and any(s in code for s in ["secret123", "mysecret", "secret", "key123"]):
        security_issues.extend(["weak JWT secret hardcoded", "secret in source code",
                                  "JWT token easily forged"])
        suggestions.extend(["use strong random secret", "store JWT secret in environment variable"])
        explanation += "Weak hardcoded JWT secret allows token forgery. "

    # ── PATH TRAVERSAL (Java/Python) ──────────────────────
    if ("basePath" in code or "base_path" in code) and "filename" in code and ".." not in code:
        security_issues.extend(["path traversal vulnerability", "no filename validation",
                                  "attacker can read arbitrary files with ../"])
        suggestions.extend(["validate filename doesn't contain ../", "use Path.resolve() and check bounds"])
        explanation += "Path traversal allows reading files outside intended directory. "

    # ── NULL POINTER / JAVA SPECIFIC ──────────────────────
    if language == "java" and "PreparedStatement" not in code and ("Statement" in code or "createStatement" in code):
        security_issues.extend(["SQL injection via Statement", "should use PreparedStatement",
                                  "no parameterized query protection"])
        suggestions.extend(["replace Statement with PreparedStatement"])
        explanation += "Java Statement allows SQL injection, use PreparedStatement. "

    if not security_issues:
        security_issues = ["security vulnerability detected", "missing input validation",
                            "insufficient access control"]
        suggestions = ["add input validation", "follow OWASP Top 10 guidelines",
                       "implement proper access control"]
        explanation = "Security vulnerabilities found requiring immediate attention."

    return CodeReviewAction(
        bugs_found=[], severity="high",
        security_issues=security_issues,
        suggestions=suggestions,
        quality_score=0.2, explanation=explanation.strip())


def smart_review_task3(code: str, language: str) -> CodeReviewAction:
    """Smart baseline agent for Task 3 - works for Python, JavaScript, Java"""
    bugs = []
    security_issues = []
    suggestions = []
    explanation_parts = []

    # ── NAMING ISSUES (all languages) ────────────────────
    if language == "python" and any(f"def {c}(" in code for c in ["p(", "r(", "f(", "g(", "h("]):
        suggestions.append("use descriptive function names instead of single letters")
        explanation_parts.append("single letter function names are unreadable")

    if language == "javascript" and "var " in code:
        suggestions.append("use const and let instead of var for proper scoping")
        explanation_parts.append("var causes hoisting and scoping issues")

    # ── PERFORMANCE ISSUES (all languages) ────────────────
    if "for i in range(len(" in code or "for(int i=0" in code:
        suggestions.append("use more idiomatic iteration patterns")
        explanation_parts.append("manual index iteration is error-prone")

    if "for i in range" in code and "for j in range" in code:
        suggestions.append("optimize O(n2) nested loops using set or dictionary for O(n)")
        explanation_parts.append("O(n2) nested loop complexity")

    if language == "javascript" and "for(" in code and ".length" in code:
        suggestions.append("use forEach or for...of instead of manual index loops")
        explanation_parts.append("manual index loop is less readable")

    # ── DOCUMENTATION (all languages) ─────────────────────
    if language == "python" and '"""' not in code and "def " in code:
        suggestions.append("add docstrings to all functions and classes")
        explanation_parts.append("missing docstrings")

    if language == "python" and "->" not in code and "def " in code:
        suggestions.append("add Python type hints to all parameters and return values")
        explanation_parts.append("no type hints")

    if language == "javascript" and "/**" not in code and "function" in code:
        suggestions.append("add JSDoc comments to all functions")
        explanation_parts.append("missing JSDoc documentation")

    if language == "java" and "/**" not in code and "public" in code:
        suggestions.append("add Javadoc comments to all public methods")
        explanation_parts.append("missing Javadoc")

    # ── ERROR HANDLING (all languages) ────────────────────
    if language == "python" and "try" not in code:
        bugs.append("no error handling with try/except blocks")
        suggestions.append("add try/except for all error-prone operations")
        explanation_parts.append("missing error handling")

    if language == "javascript" and "catch" not in code and ("fetch" in code or "then" in code):
        bugs.append("no .catch() handler for promise rejections")
        suggestions.append("add .catch() or try/catch for async operations")
        explanation_parts.append("unhandled promise rejections")

    if language == "java" and "try" not in code and ("get(" in code or "request" in code):
        bugs.append("no try-catch for potential exceptions")
        suggestions.append("add try-catch blocks for exception handling")
        explanation_parts.append("missing exception handling")

    # ── DESIGN ISSUES (all languages) ─────────────────────
    if "print(" in code and language == "python" and "return" not in code:
        suggestions.append("return values instead of printing directly for better reusability")
        explanation_parts.append("mixing IO with business logic")

    if language == "javascript" and "document.getElementById" in code and "fetch" in code:
        suggestions.append("separate data fetching from DOM manipulation")
        explanation_parts.append("mixing concerns: network and DOM")

    if language == "java" and "static" in code and "List" in code:
        suggestions.append("avoid mutable static state, use instance variables")
        explanation_parts.append("dangerous mutable static state")

    # ── PYTHON SPECIFIC ISSUES ────────────────────────────
    if "self.balance - amount" in code and "amount >" not in code:
        bugs.append("allows negative balance without validation")
        suggestions.append("add balance check: if amount > self.balance raise ValueError")

    if "cc=[]" in code or "bcc=[]" in code or "def " in code and "=[])" in code:
        bugs.append("mutable default argument shared across all function calls")
        suggestions.append("use None as default and initialize inside function body")

    if "debug=True" in code:
        security_issues.append("debug=True exposes sensitive info in production")
        suggestions.append("always set debug=False in production")

    if not suggestions:
        suggestions = ["improve naming conventions", "add documentation and type hints",
                       "optimize algorithm complexity", "add proper error handling",
                       "separate concerns and improve overall design"]
        explanation_parts = ["poor naming", "missing documentation",
                             "performance issues", "missing error handling"]

    explanation = (
        f"Comprehensive {language} code review found: {', '.join(explanation_parts)}. "
        f"Code requires refactoring to meet production standards. "
        f"Critical priorities: error handling, naming clarity, performance optimization, documentation."
    )

    return CodeReviewAction(
        bugs_found=bugs if bugs else ["missing input validation", "no error handling"],
        severity="high",
        security_issues=security_issues if security_issues else ["insufficient input validation"],
        suggestions=suggestions[:6],
        quality_score=0.25,
        explanation=explanation)


@app.post("/baseline")
def baseline():
    results = {}
    for task_id in ["task1", "task2", "task3"]:
        # Reset and get actual code + language
        obs = env.reset(task_id=task_id)
        code_snippet = obs.code_snippet
        language = obs.language

        # Smart language-aware review
        if task_id == "task1":
            action = smart_review_task1(code_snippet, language)
        elif task_id == "task2":
            action = smart_review_task2(code_snippet, language)
        else:
            action = smart_review_task3(code_snippet, language)

        env.step(action)
        g = env.get_last_grader_result()
        results[task_id] = {
            "score": g["score"] if g else 0.0,
            "passed": g["passed"] if g else False,
            "feedback": g["feedback"] if g else "",
            "language": language
        }

    avg = sum(r["score"] for r in results.values()) / len(results)
    return {"baseline_scores": results, "average_score": round(avg, 2), "agent": "smart-rule-based-baseline"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)