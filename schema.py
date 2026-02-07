"""
Pydantic models for Resume validation.
Ensures schema integrity after every edit.
"""

from pydantic import BaseModel, Field
from typing import List


class Experience(BaseModel):
    """Model for work experience entries."""
    id: str = Field(..., description="Unique identifier (e.g., exp_1)")
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job title/role")
    dates: str = Field(..., description="Employment period")
    bullets: List[str] = Field(default_factory=list, description="List of bullet points")


class Project(BaseModel):
    """Model for project entries."""
    id: str = Field(..., description="Unique identifier (e.g., proj_1)")
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")


class Education(BaseModel):
    """Model for education entries."""
    id: str = Field(..., description="Unique identifier (e.g., edu_1)")
    degree: str = Field(..., description="Degree/certification name")
    institution: str = Field(..., description="Institution name")
    year: str = Field(..., description="Year or period")


class Resume(BaseModel):
    """Complete resume model with all sections."""
    summary: str = Field(..., description="Professional summary")
    experiences: List[Experience] = Field(default_factory=list, description="Work experiences")
    skills: List[str] = Field(default_factory=list, description="Skills list")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    education: List[Education] = Field(default_factory=list, description="Education history")
