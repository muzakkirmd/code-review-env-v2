from typing import List, Optional
from pydantic import BaseModel, Field


class CodeReviewAction(BaseModel):
    bugs_found: List[str] = Field(default_factory=list)
    severity: str = Field(default="low")
    security_issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.5, ge=0.0, le=1.0)
    explanation: str = Field(default="")


class CodeReviewObservation(BaseModel):
    code_snippet: str = Field(default="")
    language: str = Field(default="python")
    task_id: str = Field(default="task1")
    task_description: str = Field(default="")
    hints: List[str] = Field(default_factory=list)
    done: bool = Field(default=False)
    reward: float = Field(default=0.0)
    feedback: str = Field(default="")
    step_count: int = Field(default=0)


class CodeReviewState(BaseModel):
    episode_id: Optional[str] = Field(default=None)
    step_count: int = Field(default=0)
    current_task: str = Field(default="task1")
    total_reward: float = Field(default=0.0)
    max_steps: int = Field(default=3)
    started_at: Optional[str] = Field(default=None)
