import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.code_review_env.models import CodeReviewAction, CodeReviewObservation, CodeReviewState
from src.code_review_env.server.environment import CodeReviewEnvironment
from tasks.task1_syntax import grade_task1
from tasks.task2_security import grade_task2
from tasks.task3_quality import grade_task3


def test_reset_returns_observation():
    env = CodeReviewEnvironment()
    obs = env.reset(task_id="task1")
    assert isinstance(obs, CodeReviewObservation)
    assert obs.task_id == "task1"
    assert obs.done == False
    assert obs.code_snippet != ""

def test_step_returns_done():
    env = CodeReviewEnvironment()
    env.reset(task_id="task1")
    action = CodeReviewAction(bugs_found=["division by zero"], severity="high", explanation="Bug found")
    obs = env.step(action)
    assert obs.done == True
    assert 0.0 <= obs.reward <= 1.0

def test_step_without_reset_raises():
    env = CodeReviewEnvironment()
    with pytest.raises(RuntimeError):
        env.step(CodeReviewAction())

def test_task1_grader_empty():
    result = grade_task1([], 0)
    assert result["score"] == 0.0
    assert result["passed"] == False

def test_task1_grader_correct():
    result = grade_task1(["division by zero when empty list"], 0)
    assert result["score"] > 0.0

def test_task2_grader_empty():
    result = grade_task2([], 0)
    assert result["score"] == 0.0

def test_task2_grader_correct():
    result = grade_task2(["SQL injection vulnerability"], 0)
    assert result["score"] > 0.0

def test_task3_grader_detailed():
    result = grade_task3(
        ["improve naming", "add docstrings", "optimize complexity"],
        "Poor naming conventions, O(n2) complexity, missing error handling and no documentation.",
        ["no error handling"], ["no input validation"], 0)
    assert result["score"] > 0.3

def test_all_scores_in_range():
    for grade_fn, args in [
        (grade_task1, (["division by zero"], 0)),
        (grade_task2, (["SQL injection"], 0)),
        (grade_task3, (["suggestion"], "explanation", [], [], 0)),
    ]:
        result = grade_fn(*args)
        assert 0.0 <= result["score"] <= 1.0
