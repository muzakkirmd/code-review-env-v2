"""
Task 2: Security Vulnerability Detection (Medium)
Features:
- 12+ security scenarios across Python, JavaScript, Java
- OWASP Top 10 coverage
- Real code execution testing for Python
"""

import subprocess
import sys
import tempfile
import os
from typing import List

# ─────────────────────────────────────────────
# PYTHON SECURITY SNIPPETS (6 snippets)
# ─────────────────────────────────────────────
PYTHON_SECURITY = [
    {
        "code": """import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

# Attacker can pass: admin' OR '1'='1
result = get_user("admin' OR '1'='1")""",
        "language": "python",
        "known_vulnerabilities": ["SQL injection", "string concatenation in SQL", "no parameterized queries", "no input sanitization"],
        "owasp": "A03:2021 Injection",
        "description": "Find the SQL injection vulnerability"
    },
    {
        "code": """import requests

API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "admin123"
SECRET_TOKEN = "my_super_secret_token_xyz"

def fetch_data():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get("https://api.example.com/data", headers=headers)
    return response.json()""",
        "language": "python",
        "known_vulnerabilities": ["hardcoded API key", "hardcoded password", "hardcoded secret token", "credentials in source code", "should use environment variables"],
        "owasp": "A02:2021 Cryptographic Failures",
        "description": "Find the hardcoded credentials vulnerability"
    },
    {
        "code": """from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/run')
def run_command():
    cmd = request.args.get('cmd')
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

app.run(debug=True)""",
        "language": "python",
        "known_vulnerabilities": ["command injection", "shell=True with user input", "no input validation", "remote code execution", "debug=True in production"],
        "owasp": "A03:2021 Injection",
        "description": "Find the command injection vulnerability"
    },
    {
        "code": """import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

@app.route('/load')
def load_data():
    data = request.args.get('data')
    decoded = base64.b64decode(data)
    obj = pickle.loads(decoded)  # DANGEROUS!
    return str(obj)""",
        "language": "python",
        "known_vulnerabilities": ["insecure deserialization", "pickle loads untrusted data", "remote code execution", "no input validation"],
        "owasp": "A08:2021 Software and Data Integrity Failures",
        "description": "Find the insecure deserialization vulnerability"
    },
    {
        "code": """from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/greet')
def greet():
    name = request.args.get('name', 'World')
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)""",
        "language": "python",
        "known_vulnerabilities": ["XSS vulnerability", "no output encoding", "user input directly in HTML", "cross site scripting", "no sanitization"],
        "owasp": "A03:2021 Injection",
        "description": "Find the XSS vulnerability"
    },
    {
        "code": """import hashlib

def store_password(password):
    # Hash the password
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed

def verify_password(password, stored_hash):
    return hashlib.md5(password.encode()).hexdigest() == stored_hash""",
        "language": "python",
        "known_vulnerabilities": ["MD5 is broken", "no salt used", "weak hashing algorithm", "should use bcrypt or argon2", "rainbow table vulnerable"],
        "owasp": "A02:2021 Cryptographic Failures",
        "description": "Find the weak password hashing vulnerability"
    },
]

# ─────────────────────────────────────────────
# JAVASCRIPT SECURITY SNIPPETS (4 snippets)
# ─────────────────────────────────────────────
JAVASCRIPT_SECURITY = [
    {
        "code": """// Express.js route
app.get('/user', (req, res) => {
    const userId = req.query.id;
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    db.query(query, (err, results) => {
        res.json(results);
    });
});""",
        "language": "javascript",
        "known_vulnerabilities": ["SQL injection", "template literal in SQL", "no parameterized queries", "user input directly in query"],
        "owasp": "A03:2021 Injection",
        "description": "Find the JavaScript SQL injection"
    },
    {
        "code": """function displayMessage(userInput) {
    document.getElementById('output').innerHTML = userInput;
}

// Called with: displayMessage('<script>alert("XSS")</script>')""",
        "language": "javascript",
        "known_vulnerabilities": ["XSS via innerHTML", "cross site scripting", "user input directly in DOM", "should use textContent or sanitize"],
        "owasp": "A03:2021 Injection",
        "description": "Find the DOM XSS vulnerability"
    },
    {
        "code": """const jwt = require('jsonwebtoken');

function createToken(userId) {
    return jwt.sign({ userId }, 'secret123', { expiresIn: '365d' });
}

function verifyToken(token) {
    return jwt.verify(token, 'secret123');
}""",
        "language": "javascript",
        "known_vulnerabilities": ["weak JWT secret", "hardcoded secret", "token expires too late", "secret in source code"],
        "owasp": "A02:2021 Cryptographic Failures",
        "description": "Find the JWT security vulnerability"
    },
    {
        "code": """app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', '*');
    res.setHeader('Access-Control-Allow-Headers', '*');
    next();
});""",
        "language": "javascript",
        "known_vulnerabilities": ["CORS misconfiguration", "wildcard origin", "allows any origin", "too permissive CORS policy"],
        "owasp": "A05:2021 Security Misconfiguration",
        "description": "Find the CORS misconfiguration"
    },
]

# ─────────────────────────────────────────────
# JAVA SECURITY SNIPPETS (2 snippets)
# ─────────────────────────────────────────────
JAVA_SECURITY = [
    {
        "code": """import java.sql.*;

public class UserDAO {
    public User findUser(String username) throws SQLException {
        Connection conn = getConnection();
        String query = "SELECT * FROM users WHERE username = '" + username + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);
        return mapToUser(rs);
    }
}""",
        "language": "java",
        "known_vulnerabilities": ["SQL injection", "string concatenation in SQL", "should use PreparedStatement", "no input validation"],
        "owasp": "A03:2021 Injection",
        "description": "Find the Java SQL injection"
    },
    {
        "code": """import java.io.*;

public class FileReader {
    public String readFile(String filename) throws IOException {
        String basePath = "/var/app/files/";
        File file = new File(basePath + filename);
        // Read and return file contents
        return new String(java.nio.file.Files.readAllBytes(file.toPath()));
    }
}

// Attacker passes: ../../etc/passwd""",
        "language": "java",
        "known_vulnerabilities": ["path traversal", "directory traversal", "no path validation", "can read any file", "should validate filename"],
        "owasp": "A01:2021 Broken Access Control",
        "description": "Find the path traversal vulnerability"
    },
]

# All snippets combined
TASK2_SNIPPETS = PYTHON_SECURITY + JAVASCRIPT_SECURITY + JAVA_SECURITY

TASK2_INFO = {
    "task_id": "task2",
    "name": "Security Vulnerability Detection",
    "description": "Identify security vulnerabilities including OWASP Top 10 issues across Python, JavaScript and Java.",
    "difficulty": "medium",
    "languages_supported": ["python", "javascript", "java"],
    "total_snippets": len(TASK2_SNIPPETS),
    "owasp_coverage": ["A01", "A02", "A03", "A05", "A08"],
    "action_schema": {
        "security_issues": "List[str] - describe each vulnerability found",
        "severity": "str - low, medium, or high",
        "suggestions": "List[str] - how to fix each issue",
        "explanation": "str - overall security assessment"
    }
}


# ─────────────────────────────────────────────
# SAFE CODE EXECUTION TESTER
# ─────────────────────────────────────────────

def test_code_execution(code: str) -> dict:
    """
    Safely execute Python code in a subprocess to detect runtime errors.
    Uses timeout to prevent infinite loops.
    Only runs code that doesn't have dangerous imports.
    """
    # Safety check - don't execute dangerous code
    dangerous = ["subprocess", "os.system", "exec(", "eval(", "pickle", "__import__"]
    for danger in dangerous:
        if danger in code:
            return {
                "executed": False,
                "reason": "Code contains potentially dangerous operations",
                "runtime_errors": []
            }

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py',
                                         delete=False) as f:
            f.write(code)
            tmp_file = f.name

        result = subprocess.run(
            [sys.executable, tmp_file],
            capture_output=True,
            text=True,
            timeout=3  # 3 second timeout
        )
        os.unlink(tmp_file)

        errors = []
        if result.returncode != 0:
            errors.append(result.stderr.strip())

        return {
            "executed": True,
            "returncode": result.returncode,
            "stdout": result.stdout[:200],
            "runtime_errors": errors,
            "has_errors": len(errors) > 0
        }
    except subprocess.TimeoutExpired:
        return {
            "executed": True,
            "runtime_errors": ["infinite loop or timeout detected"],
            "has_errors": True
        }
    except Exception as e:
        return {
            "executed": False,
            "runtime_errors": [str(e)],
            "has_errors": True
        }


# ─────────────────────────────────────────────
# GRADER
# ─────────────────────────────────────────────

def grade_task2(action_security: List[str], snippet_index: int = 0) -> dict:
    """
    Grade security vulnerability detection with execution testing bonus.
    """
    if snippet_index >= len(TASK2_SNIPPETS):
        snippet_index = 0

    snippet = TASK2_SNIPPETS[snippet_index]
    known = snippet["known_vulnerabilities"]
    language = snippet["language"]
    owasp = snippet.get("owasp", "Unknown")

    if not action_security:
        return {
            "score": 0.0,
            "passed": False,
            "feedback": f"No vulnerabilities identified! This code has serious {owasp} issues!",
            "details": {"found": 0, "total": len(known)}
        }

    # Match reported vulnerabilities
    found = 0
    matched = []
    for reported in action_security:
        r = reported.lower()
        for vuln in known:
            kws = vuln.lower().split()
            if sum(1 for kw in kws if kw in r) >= 2 or vuln.lower() in r:
                found += 1
                matched.append(vuln)
                break

    base_score = 0.1 if found == 0 and action_security else min(1.0, found / max(1, len(known)))

    # Execution testing bonus for Python
    exec_bonus = 0.0
    exec_result = {}
    if language == "python":
        exec_result = test_code_execution(snippet["code"])
        # If agent mentions runtime errors that we actually found, give bonus
        if exec_result.get("has_errors") and action_security:
            for reported in action_security:
                if any(kw in reported.lower() for kw in ["crash", "error", "exception", "runtime"]):
                    exec_bonus = 0.05
                    break

    final_score = min(1.0, base_score + exec_bonus)
    passed = final_score >= 0.5

    if found == 0:
        feedback = f"Vulnerabilities not identified. Look for {owasp} issues."
    elif found < len(known):
        feedback = f"Found {found}/{len(known)} vulnerabilities. Keep analyzing!"
    else:
        feedback = f"Excellent! All vulnerabilities found! ({owasp})"

    return {
        "score": round(final_score, 2),
        "passed": passed,
        "feedback": feedback,
        "details": {
            "found": found,
            "total": len(known),
            "matched": matched,
            "language": language,
            "owasp_category": owasp,
            "execution_test": exec_result,
            "exec_bonus": exec_bonus
        }
    }
