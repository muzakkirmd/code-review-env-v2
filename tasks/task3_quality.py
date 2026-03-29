"""
Task 3: Comprehensive Code Quality Review (Hard)
Features:
- 10+ snippets across Python, JavaScript, Java
- Real code execution for Python snippets
- AST-based complexity analysis
- Multi-dimensional scoring
"""

import ast
import subprocess
import sys
import tempfile
import os
from typing import List, Dict

# ─────────────────────────────────────────────
# PYTHON QUALITY SNIPPETS (6 snippets)
# ─────────────────────────────────────────────
PYTHON_QUALITY = [
    {
        "code": """def p(d):
    r = []
    for i in range(len(d)):
        for j in range(len(d)):
            if i != j:
                if d[i] == d[j]:
                    if d[i] not in r:
                        r.append(d[i])
    return r

x = p([1,2,3,2,4,3,5])
print(x)""",
        "language": "python",
        "quality_issues": {
            "naming": ["single letter names", "no descriptive variable names"],
            "performance": ["O(n2) complexity", "nested loops unnecessary", "set would be O(n)"],
            "documentation": ["no docstring", "no type hints", "no comments"],
            "design": ["overcomplicated logic", "one liner with set possible"],
            "error_handling": ["no input validation", "no type checking"]
        },
        "description": "Full quality review of a poorly written duplicate finder"
    },
    {
        "code": """import requests, time

def get_all_users():
    users = []
    page = 1
    while True:
        response = requests.get(f'http://api.example.com/users?page={page}')
        data = response.json()
        users.extend(data['users'])
        if len(data['users']) < 100:
            break
        page += 1
        time.sleep(0.1)
    return users

def process_users():
    users = get_all_users()
    for user in users:
        print(user['name'] + ' - ' + user['email'])""",
        "language": "python",
        "quality_issues": {
            "error_handling": ["no try except", "no timeout", "KeyError possible"],
            "performance": ["loads all users to memory", "no pagination limit", "blocking sleep"],
            "documentation": ["no docstring", "no type hints"],
            "design": ["mixing IO with processing", "no separation of concerns"],
            "security": ["hardcoded URL", "no authentication headers"]
        },
        "description": "Review an API client with multiple quality problems"
    },
    {
        "code": """class BankAccount:
    def __init__(self):
        self.balance = 0
    
    def deposit(self, amount):
        self.balance = self.balance + amount
    
    def withdraw(self, amount):
        self.balance = self.balance - amount
    
    def get_balance(self):
        return self.balance

account = BankAccount()
account.deposit(100)
account.withdraw(200)  # Goes negative!
print(account.get_balance())  # -100""",
        "language": "python",
        "quality_issues": {
            "error_handling": ["no balance check", "allows negative balance", "no validation"],
            "design": ["no transaction history", "no overdraft protection"],
            "naming": ["could be more descriptive"],
            "documentation": ["no docstring", "no type hints"],
            "performance": ["balance could be property"]
        },
        "description": "Review a bank account class with design flaws"
    },
    {
        "code": """def send_email(to, subject, body, cc=[], bcc=[]):
    # Build email
    recipients = [to] + cc + bcc
    print(f"Sending to {recipients}: {subject}")
    # ... send logic

send_email("a@b.com", "Hello", "World")
send_email("c@d.com", "Hi", "There", cc=["e@f.com"])""",
        "language": "python",
        "quality_issues": {
            "design": ["mutable default argument", "cc=[] is dangerous", "shared across calls"],
            "documentation": ["no docstring", "no type hints"],
            "error_handling": ["no email validation", "no error handling"],
            "naming": ["body could be message"],
            "performance": ["no rate limiting"]
        },
        "description": "Review email function with mutable default argument bug"
    },
    {
        "code": """import os

def get_config():
    config = {}
    config['db_host'] = 'localhost'
    config['db_port'] = 5432
    config['db_name'] = 'myapp'
    config['db_user'] = 'admin'
    config['db_pass'] = 'password123'
    config['api_key'] = 'abc123xyz'
    config['debug'] = True
    return config

settings = get_config()""",
        "language": "python",
        "quality_issues": {
            "security": ["hardcoded credentials", "password in code", "api key exposed"],
            "design": ["should use environment variables", "should use dotenv", "no config validation"],
            "documentation": ["no docstring", "no type hints"],
            "error_handling": ["no missing config handling"],
            "naming": ["config values not typed"]
        },
        "description": "Review config function with security and design issues"
    },
    {
        "code": """def calculate(a, b, op):
    if op == 'add':
        return a + b
    elif op == 'sub':
        return a - b
    elif op == 'mul':
        return a * b
    elif op == 'div':
        return a / b
    elif op == 'mod':
        return a % b
    elif op == 'pow':
        return a ** b

result = calculate(10, 0, 'div')
print(result)""",
        "language": "python",
        "quality_issues": {
            "error_handling": ["division by zero", "no zero check", "no invalid op handling"],
            "design": ["long if-elif chain", "should use dictionary dispatch", "not extensible"],
            "documentation": ["no docstring", "no type hints"],
            "naming": ["op should be operation", "a and b too short"],
            "performance": ["dictionary would be cleaner"]
        },
        "description": "Review a calculator with error handling and design issues"
    },
]

# ─────────────────────────────────────────────
# JAVASCRIPT QUALITY SNIPPETS (2 snippets)
# ─────────────────────────────────────────────
JAVASCRIPT_QUALITY = [
    {
        "code": """function fetchUserData(userId) {
    fetch('/api/users/' + userId)
        .then(response => response.json())
        .then(data => {
            document.getElementById('name').innerHTML = data.name;
            document.getElementById('email').innerHTML = data.email;
            console.log('User loaded');
        });
}

fetchUserData(123);""",
        "language": "javascript",
        "quality_issues": {
            "error_handling": ["no catch block", "no error handling", "network errors ignored"],
            "security": ["innerHTML XSS risk", "should use textContent"],
            "design": ["no loading state", "no async await"],
            "documentation": ["no JSDoc", "no parameter types"],
            "performance": ["no caching", "no debouncing"]
        },
        "description": "Review JavaScript fetch function with multiple issues"
    },
    {
        "code": """var userData = [];

function addUser(name, email) {
    userData.push({name: name, email: email});
}

function getUsers() {
    return userData;
}

function clearUsers() {
    userData = [];
}""",
        "language": "javascript",
        "quality_issues": {
            "design": ["global mutable state", "var instead of const/let", "no encapsulation"],
            "documentation": ["no JSDoc comments", "no parameter types"],
            "error_handling": ["no input validation", "no duplicate check"],
            "naming": ["could use class pattern"],
            "performance": ["no indexing for lookup"]
        },
        "description": "Review JavaScript module with global state issues"
    },
]

# ─────────────────────────────────────────────
# JAVA QUALITY SNIPPETS (2 snippets)
# ─────────────────────────────────────────────
JAVA_QUALITY = [
    {
        "code": """public class UserService {
    private static UserService instance;
    private List<User> users = new ArrayList<>();
    
    public static UserService getInstance() {
        if (instance == null) {
            instance = new UserService();
        }
        return instance;
    }
    
    public void addUser(User user) {
        users.add(user);
    }
    
    public List<User> getUsers() {
        return users;
    }
}""",
        "language": "java",
        "quality_issues": {
            "design": ["non-thread-safe singleton", "returns mutable list", "no defensive copy"],
            "error_handling": ["no null check", "no validation"],
            "documentation": ["no Javadoc", "no method comments"],
            "naming": ["clear intent but could be improved"],
            "performance": ["not synchronized"]
        },
        "description": "Review Java singleton with thread safety issues"
    },
    {
        "code": """public class DataProcessor {
    public void processData(String[] data) {
        for(int i=0; i<data.length; i++) {
            String item = data[i];
            String trimmed = item.trim();
            String upper = trimmed.toUpperCase();
            String result = upper.replace(" ", "_");
            System.out.println(result);
        }
    }
}""",
        "language": "java",
        "quality_issues": {
            "performance": ["unnecessary intermediate variables", "could chain methods"],
            "design": ["should return results not print", "no separation of concerns"],
            "documentation": ["no Javadoc", "method unclear"],
            "error_handling": ["no null check on data", "no null check on items"],
            "naming": ["processData too generic"]
        },
        "description": "Review Java data processor with design issues"
    },
]

# All snippets combined
TASK3_SNIPPETS = PYTHON_QUALITY + JAVASCRIPT_QUALITY + JAVA_QUALITY

TASK3_INFO = {
    "task_id": "task3",
    "name": "Comprehensive Code Quality Review",
    "description": "Full code review covering naming, performance, error handling, documentation, security, and design across Python, JavaScript and Java.",
    "difficulty": "hard",
    "languages_supported": ["python", "javascript", "java"],
    "total_snippets": len(TASK3_SNIPPETS),
    "action_schema": {
        "bugs_found": "List[str] - bugs found",
        "security_issues": "List[str] - security problems",
        "suggestions": "List[str] - at least 3 improvement suggestions",
        "severity": "str - overall severity: low, medium, high",
        "quality_score": "float - your estimate of code quality 0.0-1.0",
        "explanation": "str - comprehensive review explanation (100+ chars)"
    }
}


# ─────────────────────────────────────────────
# AST COMPLEXITY ANALYZER
# ─────────────────────────────────────────────

def analyze_complexity(code: str) -> Dict:
    """
    Analyze Python code complexity using AST.
    Returns cyclomatic complexity estimate and other metrics.
    """
    try:
        tree = ast.parse(code)
        complexity = 1
        functions = []
        classes = []
        nesting_depth = [0]
        max_depth = [0]

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For,
                                  ast.ExceptHandler, ast.With)):
                complexity += 1
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return {
            "cyclomatic_complexity": complexity,
            "functions": functions,
            "classes": classes,
            "lines": len(code.split('\n')),
            "high_complexity": complexity > 5
        }
    except:
        return {"cyclomatic_complexity": 0, "error": "Could not analyze"}


def run_code_safely(code: str) -> Dict:
    """
    Safely run Python code and capture output and errors.
    """
    dangerous = ["subprocess", "os.system", "exec(", "eval(", "pickle",
                  "__import__", "open(", "requests"]
    for danger in dangerous:
        if danger in code:
            return {"executed": False, "reason": "Contains external operations"}

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp = f.name

        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True, text=True, timeout=3
        )
        os.unlink(tmp)

        return {
            "executed": True,
            "returncode": result.returncode,
            "stdout": result.stdout[:300],
            "stderr": result.stderr[:300],
            "has_errors": result.returncode != 0,
            "runtime_errors": [result.stderr.strip()] if result.returncode != 0 else []
        }
    except subprocess.TimeoutExpired:
        return {"executed": True, "has_errors": True,
                "runtime_errors": ["Timeout - possible infinite loop"]}
    except Exception as e:
        return {"executed": False, "has_errors": True, "runtime_errors": [str(e)]}


# ─────────────────────────────────────────────
# GRADER
# ─────────────────────────────────────────────

def grade_task3(action_suggestions: List[str], action_explanation: str,
                action_bugs: List[str], action_security: List[str],
                snippet_index: int = 0) -> dict:
    """
    Grade comprehensive code review with AST analysis and execution testing.
    """
    if snippet_index >= len(TASK3_SNIPPETS):
        snippet_index = 0

    snippet = TASK3_SNIPPETS[snippet_index]
    quality_issues = snippet["quality_issues"]
    language = snippet["language"]
    all_issues = [i for issues in quality_issues.values() for i in issues]
    all_text = " ".join(action_suggestions + action_bugs +
                        action_security + [action_explanation]).lower()

    # Score 1: Issue coverage (30%)
    hits = sum(1 for issue in all_issues
               if any(kw in all_text for kw in issue.lower().split() if len(kw) > 4))
    suggestion_score = min(1.0, hits / max(1, len(all_issues) * 0.4))

    # Score 2: Category coverage (30%)
    category_score = sum(
        1 for issues in quality_issues.values()
        if any(kw in all_text for issue in issues
               for kw in issue.lower().split() if len(kw) > 4)
    ) / len(quality_issues)

    # Score 3: Explanation depth (20%)
    exp_score = (1.0 if len(action_explanation) > 200 else
                 0.7 if len(action_explanation) > 100 else
                 0.4 if len(action_explanation) > 50 else
                 0.2 if action_explanation else 0.0)

    # Score 4: Quantity of findings (20%)
    qty = len(action_suggestions) + len(action_bugs) + len(action_security)
    qty_score = min(1.0, qty / 5)

    base = suggestion_score * 0.30 + category_score * 0.30 + exp_score * 0.20 + qty_score * 0.20

    # AST complexity bonus for Python
    ast_bonus = 0.0
    ast_result = {}
    exec_result = {}

    if language == "python":
        ast_result = analyze_complexity(snippet["code"])
        exec_result = run_code_safely(snippet["code"])

        # Bonus if agent mentions complexity issues that AST confirmed
        if ast_result.get("high_complexity"):
            if any(kw in all_text for kw in ["complex", "complexity", "nested", "refactor"]):
                ast_bonus += 0.05

        # Bonus if agent mentions runtime errors that execution confirmed
        if exec_result.get("has_errors"):
            if any(kw in all_text for kw in ["crash", "error", "exception", "fails"]):
                ast_bonus += 0.05

    final = min(1.0, base + ast_bonus)
    passed = final >= 0.5

    feedback = ("Outstanding comprehensive review!" if final >= 0.8 else
                "Good review! Covered most issues." if final >= 0.6 else
                "Partial review. More depth needed." if final >= 0.4 else
                "Incomplete review. More analysis required.")

    return {
        "score": round(final, 2),
        "passed": passed,
        "feedback": f"{feedback} Score: {final:.2f}",
        "details": {
            "category_score": round(category_score, 2),
            "suggestion_score": round(suggestion_score, 2),
            "explanation_score": round(exp_score, 2),
            "items_raised": qty,
            "language": language,
            "ast_analysis": ast_result,
            "execution_test": exec_result,
            "ast_bonus": ast_bonus
        }
    }
