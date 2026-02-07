"""
Tool functions for resume editing.
Each tool does ONE thing, preserves JSON structure, and validates after changes.
"""

import json
from pathlib import Path
from typing import Optional
from schema import Resume, Experience, Project, Education


# Path to resume file
RESUME_FILE = Path(__file__).parent / "resume.json"


def _load_resume() -> dict:
    """Load resume data from JSON file."""
    with open(RESUME_FILE, "r") as f:
        return json.load(f)


def _save_resume(data: dict) -> str:
    """Save resume data to JSON file after validation."""
    # Validate with Pydantic before saving
    Resume(**data)
    with open(RESUME_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return "Resume saved successfully."


# ============== READ TOOLS ==============

def get_resume() -> dict:
    """
    Get the complete resume JSON.
    Returns the full resume data structure.
    """
    return _load_resume()


def get_section(section_name: str) -> str:
    """
    Get a specific section from the resume.
    
    Args:
        section_name: One of 'summary', 'experiences', 'skills', 'projects', 'education'
    
    Returns:
        The section data as a formatted string.
    """
    data = _load_resume()
    valid_sections = ["summary", "experiences", "skills", "projects", "education"]
    
    if section_name not in valid_sections:
        return f"Error: Invalid section '{section_name}'. Valid sections: {valid_sections}"
    
    section_data = data.get(section_name)
    return json.dumps(section_data, indent=2)


# ============== SUMMARY TOOLS ==============

def get_summary() -> str:
    """
    Get the current professional summary.
    
    Returns:
        The summary text.
    """
    data = _load_resume()
    return data.get("summary", "")


def update_summary(new_summary: str) -> str:
    """
    Update the professional summary.
    
    Args:
        new_summary: The new summary text to set.
    
    Returns:
        Success or error message.
    """
    if not new_summary or not new_summary.strip():
        return "Error: Summary cannot be empty."
    
    data = _load_resume()
    data["summary"] = new_summary.strip()
    return _save_resume(data)


# ============== EXPERIENCE TOOLS ==============

def get_experiences() -> str:
    """
    Get all work experiences.
    
    Returns:
        JSON string of all experiences.
    """
    data = _load_resume()
    return json.dumps(data.get("experiences", []), indent=2)


def get_experience_by_id(experience_id: str) -> str:
    """
    Get a specific experience by ID.
    
    Args:
        experience_id: The experience ID (e.g., 'exp_1')
    
    Returns:
        JSON string of the experience or error message.
    """
    data = _load_resume()
    for exp in data.get("experiences", []):
        if exp["id"] == experience_id:
            return json.dumps(exp, indent=2)
    return f"Error: Experience with ID '{experience_id}' not found."


def update_experience(experience_id: str, company: Optional[str] = None, 
                      role: Optional[str] = None, dates: Optional[str] = None) -> str:
    """
    Update an existing experience entry.
    
    Args:
        experience_id: The experience ID to update
        company: New company name (optional)
        role: New role/title (optional)
        dates: New dates (optional)
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    for exp in data.get("experiences", []):
        if exp["id"] == experience_id:
            if company:
                exp["company"] = company
            if role:
                exp["role"] = role
            if dates:
                exp["dates"] = dates
            return _save_resume(data)
    return f"Error: Experience with ID '{experience_id}' not found."


def add_experience(company: str, role: str, dates: str, bullets: Optional[list] = None) -> str:
    """
    Add a new experience entry.
    
    Args:
        company: Company name
        role: Job title/role
        dates: Employment period
        bullets: List of bullet points (optional)
    
    Returns:
        Success message with the new experience ID.
    """
    data = _load_resume()
    experiences = data.get("experiences", [])
    
    # Generate new ID
    existing_ids = [int(e["id"].split("_")[1]) for e in experiences if e["id"].startswith("exp_")]
    new_id = f"exp_{max(existing_ids, default=0) + 1}"
    
    new_exp = {
        "id": new_id,
        "company": company,
        "role": role,
        "dates": dates,
        "bullets": bullets or []
    }
    
    experiences.insert(0, new_exp)  # Add to beginning
    data["experiences"] = experiences
    _save_resume(data)
    return f"Experience added successfully with ID: {new_id}"


def remove_experience(experience_id: str) -> str:
    """
    Remove an experience entry.
    
    Args:
        experience_id: The experience ID to remove
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    experiences = data.get("experiences", [])
    original_len = len(experiences)
    
    data["experiences"] = [e for e in experiences if e["id"] != experience_id]
    
    if len(data["experiences"]) == original_len:
        return f"Error: Experience with ID '{experience_id}' not found."
    
    return _save_resume(data)


def add_bullet(experience_id: str, bullet: str) -> str:
    """
    Add a bullet point to an experience.
    
    Args:
        experience_id: The experience ID
        bullet: The bullet point text to add
    
    Returns:
        Success or error message.
    """
    if not bullet or not bullet.strip():
        return "Error: Bullet text cannot be empty."
    
    data = _load_resume()
    for exp in data.get("experiences", []):
        if exp["id"] == experience_id:
            exp["bullets"].append(bullet.strip())
            return _save_resume(data)
    return f"Error: Experience with ID '{experience_id}' not found."


def update_bullet(experience_id: str, bullet_index: int, new_bullet: str) -> str:
    """
    Update a specific bullet point in an experience.
    
    Args:
        experience_id: The experience ID
        bullet_index: The index of the bullet to update (0-based)
        new_bullet: The new bullet text
    
    Returns:
        Success or error message.
    """
    if not new_bullet or not new_bullet.strip():
        return "Error: Bullet text cannot be empty."
    
    data = _load_resume()
    for exp in data.get("experiences", []):
        if exp["id"] == experience_id:
            if 0 <= bullet_index < len(exp["bullets"]):
                exp["bullets"][bullet_index] = new_bullet.strip()
                return _save_resume(data)
            return f"Error: Bullet index {bullet_index} out of range. Experience has {len(exp['bullets'])} bullets."
    return f"Error: Experience with ID '{experience_id}' not found."


def remove_bullet(experience_id: str, bullet_index: int) -> str:
    """
    Remove a bullet point from an experience.
    
    Args:
        experience_id: The experience ID
        bullet_index: The index of the bullet to remove (0-based)
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    for exp in data.get("experiences", []):
        if exp["id"] == experience_id:
            if 0 <= bullet_index < len(exp["bullets"]):
                removed = exp["bullets"].pop(bullet_index)
                _save_resume(data)
                return f"Bullet removed: '{removed[:50]}...'" if len(removed) > 50 else f"Bullet removed: '{removed}'"
            return f"Error: Bullet index {bullet_index} out of range. Experience has {len(exp['bullets'])} bullets."
    return f"Error: Experience with ID '{experience_id}' not found."


# ============== SKILLS TOOLS ==============

def get_skills() -> str:
    """
    Get all skills.
    
    Returns:
        JSON string of all skills.
    """
    data = _load_resume()
    return json.dumps(data.get("skills", []), indent=2)


def add_skill(skill: str) -> str:
    """
    Add a new skill.
    
    Args:
        skill: The skill to add
    
    Returns:
        Success or error message.
    """
    if not skill or not skill.strip():
        return "Error: Skill cannot be empty."
    
    data = _load_resume()
    skills = data.get("skills", [])
    
    skill = skill.strip()
    if skill in skills:
        return f"Skill '{skill}' already exists."
    
    skills.append(skill)
    data["skills"] = skills
    return _save_resume(data)


def remove_skill(skill: str) -> str:
    """
    Remove a skill.
    
    Args:
        skill: The skill to remove
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    skills = data.get("skills", [])
    
    skill = skill.strip()
    if skill not in skills:
        return f"Error: Skill '{skill}' not found."
    
    skills.remove(skill)
    data["skills"] = skills
    return _save_resume(data)


# ============== PROJECTS TOOLS ==============

def get_projects() -> str:
    """
    Get all projects.
    
    Returns:
        JSON string of all projects.
    """
    data = _load_resume()
    return json.dumps(data.get("projects", []), indent=2)


def get_project_by_id(project_id: str) -> str:
    """
    Get a specific project by ID.
    
    Args:
        project_id: The project ID (e.g., 'proj_1')
    
    Returns:
        JSON string of the project or error message.
    """
    data = _load_resume()
    for proj in data.get("projects", []):
        if proj["id"] == project_id:
            return json.dumps(proj, indent=2)
    return f"Error: Project with ID '{project_id}' not found."


def add_project(name: str, description: str) -> str:
    """
    Add a new project.
    
    Args:
        name: Project name
        description: Project description
    
    Returns:
        Success message with the new project ID.
    """
    if not name or not name.strip():
        return "Error: Project name cannot be empty."
    if not description or not description.strip():
        return "Error: Project description cannot be empty."
    
    data = _load_resume()
    projects = data.get("projects", [])
    
    # Generate new ID
    existing_ids = [int(p["id"].split("_")[1]) for p in projects if p["id"].startswith("proj_")]
    new_id = f"proj_{max(existing_ids, default=0) + 1}"
    
    new_proj = {
        "id": new_id,
        "name": name.strip(),
        "description": description.strip()
    }
    
    projects.append(new_proj)
    data["projects"] = projects
    _save_resume(data)
    return f"Project added successfully with ID: {new_id}"


def update_project(project_id: str, name: Optional[str] = None, description: Optional[str] = None) -> str:
    """
    Update an existing project.
    
    Args:
        project_id: The project ID to update
        name: New project name (optional)
        description: New description (optional)
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    for proj in data.get("projects", []):
        if proj["id"] == project_id:
            if name:
                proj["name"] = name.strip()
            if description:
                proj["description"] = description.strip()
            return _save_resume(data)
    return f"Error: Project with ID '{project_id}' not found."


def remove_project(project_id: str) -> str:
    """
    Remove a project.
    
    Args:
        project_id: The project ID to remove
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    projects = data.get("projects", [])
    original_len = len(projects)
    
    data["projects"] = [p for p in projects if p["id"] != project_id]
    
    if len(data["projects"]) == original_len:
        return f"Error: Project with ID '{project_id}' not found."
    
    return _save_resume(data)


# ============== EDUCATION TOOLS ==============

def get_education() -> str:
    """
    Get all education entries.
    
    Returns:
        JSON string of all education entries.
    """
    data = _load_resume()
    return json.dumps(data.get("education", []), indent=2)


def get_education_by_id(education_id: str) -> str:
    """
    Get a specific education entry by ID.
    
    Args:
        education_id: The education ID (e.g., 'edu_1')
    
    Returns:
        JSON string of the education entry or error message.
    """
    data = _load_resume()
    for edu in data.get("education", []):
        if edu["id"] == education_id:
            return json.dumps(edu, indent=2)
    return f"Error: Education with ID '{education_id}' not found."


def update_education(education_id: str, degree: Optional[str] = None, 
                     institution: Optional[str] = None, year: Optional[str] = None) -> str:
    """
    Update an existing education entry.
    
    Args:
        education_id: The education ID to update
        degree: New degree name (optional)
        institution: New institution name (optional)
        year: New year/period (optional)
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    for edu in data.get("education", []):
        if edu["id"] == education_id:
            if degree:
                edu["degree"] = degree.strip()
            if institution:
                edu["institution"] = institution.strip()
            if year:
                edu["year"] = year.strip()
            return _save_resume(data)
    return f"Error: Education with ID '{education_id}' not found."


def add_education(degree: str, institution: str, year: str) -> str:
    """
    Add a new education entry.
    
    Args:
        degree: Degree/certification name
        institution: Institution name
        year: Year or period
    
    Returns:
        Success message with the new education ID.
    """
    if not degree or not degree.strip():
        return "Error: Degree cannot be empty."
    if not institution or not institution.strip():
        return "Error: Institution cannot be empty."
    if not year or not year.strip():
        return "Error: Year cannot be empty."
    
    data = _load_resume()
    education = data.get("education", [])
    
    # Generate new ID
    existing_ids = [int(e["id"].split("_")[1]) for e in education if e["id"].startswith("edu_")]
    new_id = f"edu_{max(existing_ids, default=0) + 1}"
    
    new_edu = {
        "id": new_id,
        "degree": degree.strip(),
        "institution": institution.strip(),
        "year": year.strip()
    }
    
    education.append(new_edu)
    data["education"] = education
    _save_resume(data)
    return f"Education added successfully with ID: {new_id}"


def remove_education(education_id: str) -> str:
    """
    Remove an education entry.
    
    Args:
        education_id: The education ID to remove
    
    Returns:
        Success or error message.
    """
    data = _load_resume()
    education = data.get("education", [])
    original_len = len(education)
    
    data["education"] = [e for e in education if e["id"] != education_id]
    
    if len(data["education"]) == original_len:
        return f"Error: Education with ID '{education_id}' not found."
    
    return _save_resume(data)
