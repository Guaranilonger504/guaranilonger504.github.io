from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Paper(StrictModel):
    base_id: str
    version: int = Field(ge=1)
    title: str
    authors: list[str]
    abstract: str
    categories: list[str]
    published: datetime
    updated: datetime
    abstract_url: str
    pdf_url: str

    @property
    def uid(self) -> str:
        return f"{self.base_id}v{self.version}"


class ScreeningResult(StrictModel):
    arxiv_id: str
    relevance_score: int = Field(ge=0, le=10)
    novelty_score: int = Field(ge=0, le=10)
    transferability_score: int = Field(ge=0, le=10)
    systems_score: int = Field(ge=0, le=10)
    confidence: float = Field(ge=0, le=1)
    priority: Literal["skip", "skim", "read", "deep_read"]
    matched_topics: list[str]
    short_summary_zh: str
    short_summary_en: str
    why_interesting_zh: str
    why_interesting_en: str
    relation_to_my_work_zh: str
    relation_to_my_work_en: str
    possible_transfer_zh: str
    possible_transfer_en: str
    possible_overlap_or_conflict_zh: str
    possible_overlap_or_conflict_en: str
    questions_to_verify_zh: list[str]
    questions_to_verify_en: list[str]


class ScreeningBatch(StrictModel):
    results: list[ScreeningResult]


class DeepAnalysis(StrictModel):
    arxiv_id: str
    research_problem_zh: str
    research_problem_en: str
    core_method_zh: str
    core_method_en: str
    contributions_zh: list[str]
    contributions_en: list[str]
    why_watch_zh: str
    why_watch_en: str
    direct_relation_zh: str
    direct_relation_en: str
    transferable_mechanisms_zh: list[str]
    transferable_mechanisms_en: list[str]
    potential_overlap_zh: str
    potential_overlap_en: str
    potential_conflict_zh: str
    potential_conflict_en: str
    full_text_questions_zh: list[str]
    full_text_questions_en: list[str]
    experiment_checks_zh: list[str]
    experiment_checks_en: list[str]
    tracking_targets: list[str]
    next_steps_zh: list[str]
    next_steps_en: list[str]


class DeepAnalysisBatch(StrictModel):
    results: list[DeepAnalysis]

