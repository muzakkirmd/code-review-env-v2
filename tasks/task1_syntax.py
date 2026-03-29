"""
Task 1: Syntax & Logic Bug Detection (Easy)
Features:
- 15+ code snippets across Python, JavaScript, Java
- Real AST analysis for Python code
- Deterministic grading
"""

import ast
from typing import List, Dict

# ─────────────────────────────────────────────
# PYTHON SNIPPETS (10 snippets)
# ─────────────────────────────────────────────
PYTHON_SNIPPETS = [
    {
        "code": """def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

result = calculate_average([])
print(result)""",
        "language": "python",
        "known_bugs": ["division by zero", "empty list", "ZeroDivisionError", "no input validation"],
        "description": "Find the bug that causes a crash with empty input"
    },
    {
        "code": """def find_max(lst):
    max_val = 0
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val

print(find_max([-5, -3, -1]))""",
        "language": "python",
        "known_bugs": ["wrong initial value", "fails for negative numbers", "max_val initialized to 0"],
        "description": "Find the logic bug with negative numbers"
    },
    {
        "code": """def count_words(sentence):
    words = sentence.split(' ')
    count = 0
    for word in words:
        count =+ 1
    return count

print(count_words("hello world"))""",
        "language": "python",
        "known_bugs": ["=+ instead of +=", "wrong operator", "count always equals 1"],
        "description": "Find the operator bug in the counter"
    },
    {
        "code": """def is_palindrome(s):
    return s == s.reverse()

print(is_palindrome("racecar"))""",
        "language": "python",
        "known_bugs": ["list reverse not string", "reverse returns None", "AttributeError", "should use s[::-1]"],
        "description": "Find the string reversal bug"
    },
    {
        "code": """def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n)

print(factorial(5))""",
        "language": "python",
        "known_bugs": ["infinite recursion", "missing n-1", "should be factorial(n-1)", "RecursionError"],
        "description": "Find the infinite recursion bug"
    },
    {
        "code": """def remove_duplicates(lst):
    for i in range(len(lst)):
        if lst[i] in lst[i+1:]:
            lst.pop(i)
    return lst

print(remove_duplicates([1, 2, 2, 3, 3]))""",
        "language": "python",
        "known_bugs": ["index out of range", "modifying list while iterating", "IndexError", "unsafe iteration"],
        "description": "Find the list mutation bug"
    },
    {
        "code": """def binary_search(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) / 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "language": "python",
        "known_bugs": ["float division instead of integer", "mid should use //", "TypeError on arr[mid]", "right should be len(arr)-1"],
        "description": "Find the binary search index bug"
    },
    {
        "code": """def flatten(lst):
    result = []
    for item in lst:
        if type(item) == list:
            result += flatten(item)
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], 5]))""",
        "language": "python",
        "known_bugs": ["type() instead of isinstance()", "fragile type check", "should use isinstance(item, list)"],
        "description": "Find the type checking anti-pattern"
    },
    {
        "code": """def get_value(dictionary, key):
    return dictionary[key]

data = {"name": "Alice", "age": 30}
print(get_value(data, "email"))""",
        "language": "python",
        "known_bugs": ["KeyError", "no default value", "missing key handling", "should use dict.get()"],
        "description": "Find the missing key error"
    },
    {
        "code": """def read_file(filename):
    f = open(filename, 'r')
    content = f.read()
    return content

print(read_file("test.txt"))""",
        "language": "python",
        "known_bugs": ["file not closed", "resource leak", "no with statement", "no error handling"],
        "description": "Find the resource leak bug"
    },
]

# ─────────────────────────────────────────────
# JAVASCRIPT SNIPPETS (3 snippets)
# ─────────────────────────────────────────────
JAVASCRIPT_SNIPPETS = [
    {
        "code": """function sumArray(arr) {
    let sum = 0;
    for (let i = 0; i <= arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

console.log(sumArray([1, 2, 3]));""",
        "language": "javascript",
        "known_bugs": ["off by one error", "i <= arr.length should be i < arr.length", "undefined access", "NaN result"],
        "description": "Find the off-by-one error in JavaScript"
    },
    {
        "code": """function isEqual(a, b) {
    return a == b;
}

console.log(isEqual(0, false));   // true?
console.log(isEqual("1", 1));     // true?""",
        "language": "javascript",
        "known_bugs": ["loose equality", "== instead of ===", "type coercion bug", "should use strict equality"],
        "description": "Find the JavaScript equality bug"
    },
    {
        "code": """var results = [];
for (var i = 0; i < 3; i++) {
    results.push(function() {
        return i;
    });
}

console.log(results[0]());  // Expected 0, got 3""",
        "language": "javascript",
        "known_bugs": ["closure bug", "var hoisting", "should use let", "all functions return 3"],
        "description": "Find the JavaScript closure bug"
    },
]

# ─────────────────────────────────────────────
# JAVA SNIPPETS (2 snippets)
# ─────────────────────────────────────────────
JAVA_SNIPPETS = [
    {
        "code": """public class StringCompare {
    public static void main(String[] args) {
        String a = new String("hello");
        String b = new String("hello");
        
        if (a == b) {
            System.out.println("Equal");
        } else {
            System.out.println("Not equal");
        }
    }
}""",
        "language": "java",
        "known_bugs": ["reference comparison", "== compares references not values", "should use .equals()", "always prints Not equal"],
        "description": "Find the Java string comparison bug"
    },
    {
        "code": """public class NullCheck {
    public static int getLength(String s) {
        return s.length();
    }
    
    public static void main(String[] args) {
        System.out.println(getLength(null));
    }
}""",
        "language": "java",
        "known_bugs": ["NullPointerException", "no null check", "should check s != null", "missing null validation"],
        "description": "Find the null pointer bug"
    },
]

# All snippets combined
TASK1_SNIPPETS = PYTHON_SNIPPETS + JAVASCRIPT_SNIPPETS + JAVA_SNIPPETS

TASK1_INFO = {
    "task_id": "task1",
    "name": "Syntax & Logic Bug Detection",
    "description": "Identify obvious bugs and logic errors in code snippets across Python, JavaScript and Java.",
    "difficulty": "easy",
    "languages_supported": ["python", "javascript", "java"],
    "total_snippets": len(TASK1_SNIPPETS),
    "action_schema": {
        "bugs_found": "List[str] - describe each bug found",
        "severity": "str - low, medium, or high",
        "explanation": "str - overall explanation of the review"
    }
}


# ─────────────────────────────────────────────
# AST ANALYZER (Python only)
# ─────────────────────────────────────────────

def analyze_python_ast(code: str) -> Dict:
    """
    Use Python's built-in AST module to analyze code structure.
    Returns detected issues from static analysis.
    """
    issues = []
    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append("bare except clause detected")

            # Check for == None instead of is None
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, ast.Eq):
                        issues.append("possible == None usage, prefer is None")
                        break

            # Check for print statements (Python 2 style)
            if isinstance(node, ast.Expr):
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        if node.value.func.id == 'print':
                            pass  # valid in Python 3

            # Check for global variables
            if isinstance(node, ast.Global):
                issues.append("global variable usage detected")

            # Check for mutable default arguments
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(f"mutable default argument in function '{node.name}'")

        return {
            "ast_valid": True,
            "issues_detected": issues,
            "node_count": len(list(ast.walk(tree)))
        }
    except SyntaxError as e:
        return {
            "ast_valid": False,
            "syntax_error": str(e),
            "issues_detected": ["syntax error in code"]
        }


# ─────────────────────────────────────────────
# GRADER
# ─────────────────────────────────────────────

def grade_task1(action_bugs: List[str], snippet_index: int = 0) -> dict:
    """
    Grade bug detection with AST analysis bonus.
    """
    if snippet_index >= len(TASK1_SNIPPETS):
        snippet_index = 0

    snippet = TASK1_SNIPPETS[snippet_index]
    known_bugs = snippet["known_bugs"]
    language = snippet["language"]

    if not action_bugs:
        return {
            "score": 0.0,
            "passed": False,
            "feedback": "No bugs identified. Look more carefully at the code!",
            "details": {"bugs_found": 0, "total_bugs": len(known_bugs)}
        }

    # Match reported bugs against known bugs
    found = 0
    matched = []
    for reported in action_bugs:
        r = reported.lower()
        for known in known_bugs:
            if any(kw in r for kw in known.lower().split() if len(kw) > 3):
                found += 1
                matched.append(known)
                break

    base_score = min(1.0, found / max(1, len(known_bugs)))

    # AST bonus for Python snippets
    ast_bonus = 0.0
    ast_result = {}
    if language == "python":
        ast_result = analyze_python_ast(snippet["code"])
        if ast_result.get("ast_valid") and ast_result.get("issues_detected"):
            # Check if agent found AST-detected issues
            ast_issues = ast_result["issues_detected"]
            for ast_issue in ast_issues:
                for reported in action_bugs:
                    if any(kw in reported.lower() for kw in ast_issue.lower().split() if len(kw) > 3):
                        ast_bonus = 0.05
                        break

    final_score = min(1.0, base_score + ast_bonus)
    passed = final_score >= 0.5

    if found == 0:
        feedback = "No relevant bugs identified."
    elif found < len(known_bugs):
        feedback = f"Found {found}/{len(known_bugs)} bugs. Keep looking!"
    else:
        feedback = "All bugs found! Excellent review!"

    return {
        "score": round(final_score, 2),
        "passed": passed,
        "feedback": feedback,
        "details": {
            "bugs_found": found,
            "total_bugs": len(known_bugs),
            "matched_bugs": matched,
            "language": language,
            "ast_analysis": ast_result,
            "ast_bonus": ast_bonus
        }
    }
