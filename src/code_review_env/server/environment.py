import uuid
import random
from datetime import datetime
from typing import Optional
from src.code_review_env.models import CodeReviewAction, CodeReviewObservation, CodeReviewState
from tasks.task1_syntax import TASK1_SNIPPETS, grade_task1
from tasks.task2_security import TASK2_SNIPPETS, grade_task2
from tasks.task3_quality import TASK3_SNIPPETS, grade_task3


class CodeReviewEnvironment:
    def __init__(self):
        self._state: Optional[CodeReviewState] = None
        self._snippet_index: int = 0
        self._current_task: str = "task1"
        self._last_grader_result = None

    def reset(self, task_id: str = "task1") -> CodeReviewObservation:
        if task_id not in ["task1", "task2", "task3"]:
            task_id = "task1"
        self._current_task = task_id
        self._snippet_index = random.randint(0, 2)
        self._last_grader_result = None
        self._state = CodeReviewState(
            episode_id=str(uuid.uuid4()), step_count=0,
            current_task=task_id, total_reward=0.0,
            max_steps=3, started_at=datetime.now().isoformat()
        )
        snippet, desc, hints = self._get_content(task_id)
        return CodeReviewObservation(
            code_snippet=snippet["code"], language=snippet["language"],
            task_id=task_id, task_description=desc, hints=hints,
            done=False, reward=0.0, feedback="Episode started. Review the code.", step_count=0
        )

    def step(self, action: CodeReviewAction) -> CodeReviewObservation:
        if self._state is None:
            raise RuntimeError("Call reset() before step()")
        self._state.step_count += 1
        grader = self._grade(action)
        self._last_grader_result = grader
        reward = self._reward(grader, action)
        self._state.total_reward += reward
        snippet, desc, _ = self._get_content(self._current_task)
        return CodeReviewObservation(
            code_snippet=snippet["code"], language=snippet["language"],
            task_id=self._current_task, task_description=desc, hints=[],
            done=True, reward=round(reward, 2),
            feedback=grader["feedback"], step_count=self._state.step_count
        )

    def state(self) -> CodeReviewState:
        return self._state if self._state else CodeReviewState()

    def get_last_grader_result(self):
        return self._last_grader_result

    def _grade(self, action: CodeReviewAction) -> dict:
        idx = self._snippet_index
        if self._current_task == "task1":
            return grade_task1(action.bugs_found, idx)
        elif self._current_task == "task2":
            return grade_task2(action.security_issues, idx)
        else:
            return grade_task3(action.suggestions, action.explanation, action.bugs_found, action.security_issues, idx)

    def _reward(self, grader: dict, action: CodeReviewAction) -> float:
        base = grader["score"] * 0.7
        exp_bonus = 0.1 if len(action.explanation) > 100 else 0.05 if len(action.explanation) > 50 else 0.0
        total = len(action.suggestions) + len(action.bugs_found) + len(action.security_issues)
        sug_bonus = 0.1 if total >= 3 else 0.05 if total >= 1 else 0.0
        s = grader["score"]
        sev_bonus = 0.1 if (s >= 0.7 and action.severity == "high") or (0.3 <= s < 0.7 and action.severity == "medium") or (s < 0.3 and action.severity == "low") else 0.0
        penalty = -0.2 if not action.bugs_found and not action.security_issues and not action.suggestions else 0.0
        return max(0.0, min(1.0, base + exp_bonus + sug_bonus + sev_bonus + penalty))

    def _get_content(self, task_id: str):
        idx = self._snippet_index
        if task_id == "task1":
            snippets = TASK1_SNIPPETS
            desc = "Find syntax errors and logic bugs in this code."
            hints = ["Look for division errors", "Check loop logic", "Think about edge cases"]
        elif task_id == "task2":
            snippets = TASK2_SNIPPETS
            desc = "Identify security vulnerabilities in this code."
            hints = ["Check for injection vulnerabilities", "Look for hardcoded credentials", "Check input validation"]
        else:
            snippets = TASK3_SNIPPETS
            desc = "Perform a comprehensive code quality review."
            hints = ["Check naming conventions", "Look for performance issues", "Check error handling and docs"]
        if idx >= len(snippets):
            idx = 0
        return snippets[idx], desc, hints
