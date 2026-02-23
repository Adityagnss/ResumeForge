# ResumeForge

Edit your resume by just talking to it. No forms, no manual editing — just tell the AI what you want changed and it handles the rest.

> Powered by **Gemini 2.0 Flash** · Built with **Google ADK**

![ResumeForge Interface](TestingPICS/Screenshot_2026-02-08_03-07-32_AM.png)

---

## Overview

ResumeForge is a multi-agent AI system for editing resumes using natural language. Instead of opening a Word document or PDF editor, you simply chat with the system:

> *"Add Python to my skills"*
> *"Make my summary sound more senior"*
> *"Add a bullet about reducing load time by 40% to my first job"*

The system understands your request, figures out which section of the resume to update, and saves the changes automatically.

Your resume lives in a `resume.json` file. All edits go through structured tools — the AI never guesses or makes things up.

---

## Key Features

- **Natural language editing** — Say what you want, the agent figures out the rest
- **Multi-agent system** — Each resume section has its own dedicated specialist agent
- **Gemini-powered** — Uses Google's Gemini 2.0 Flash model for fast, accurate responses
- **Safe edits** — Every change is validated against a strict schema before saving
- **No hallucinations** — Agents only read/write using tools, not memory
- **Web UI included** — Clean chat interface via `adk web`, no frontend coding needed
- **Section-aware routing** — Requests automatically get sent to the right specialist
- **Instant feedback** — Confirmation after every change so you know it worked

---

## System Architecture

ResumeForge uses a layered agent structure. Each layer has one job:

```
User Input
    │
    ▼
┌─────────────┐
│   Unibot    │  ← Greets you, understands what you want
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ ResumeAgent  │  ← Figures out which section to edit, routes the request
└──────┬───────┘
       │
  ┌────┴─────────────────────────────┐
  │                                  │
  ▼          ▼          ▼           ▼           ▼
Summary   Experience  Skills    Projects   Education
 Agent      Agent      Agent     Agent      Agent
  │           │          │         │          │
  ▼           ▼          ▼         ▼          ▼
           resume.json (single source of truth)
```

Every agent reads from and writes to `resume.json` via tools. No agent edits data directly.

---

## Technical Stack

| Component        | Technology              |
|------------------|-------------------------|
| Agent Framework  | Google ADK              |
| LLM              | Gemini 2.0 Flash        |
| Data Validation  | Pydantic v2             |
| Data Storage     | JSON (`resume.json`)    |
| Web UI           | ADK built-in web server |
| Language         | Python 3.11+            |

---

## Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/Adityagnss/ResumeForge.git
cd ResumeForge/resume_agent
```

### Step 2 — Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate        # Windows
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up your API key

```bash
cp .env.example .env
```

Open `.env` and paste your Gemini API key (see [Configuration](#configuration) below).

### Step 5 — Run

```bash
adk web
```

Open your browser at [http://localhost:8000](http://localhost:8000).

![Running the app](TestingPICS/Screenshot_2026-02-08_03-07-58_AM.png)

---

## Configuration

Get a free Gemini API key from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

Your `.env` file should look like this:

```env
GOOGLE_API_KEY=your_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

That's it — no other setup needed.

> **Note:** The `.env` file is listed in `.gitignore` and will never be committed to GitHub.

---

## Usage

Once the app is running, open [http://localhost:8000](http://localhost:8000) and start chatting.

**Select the `unibot` agent** from the dropdown if it isn't already selected.

### Things you can say:

```
"Hello"
"What can you do?"
"Show me my current skills"
"Add Python to my skills"
"Remove Java from my skills"
"Make my summary more concise"
"Update my first job's company name to Google"
"Add a bullet about leading a team of 5 engineers to my second job"
"Add a new project called TaskBot with description: AI task manager"
"Update my B.Tech degree to M.Tech"
```

![Example chat interaction](TestingPICS/Screenshot_2026-02-08_03-12-45_AM.png)

---

## Agent Hierarchy

There are 7 agents in total. Here's what each one does:

| Agent | Role |
|-------|------|
| **Unibot** | Entry point. Greets users and routes resume requests to ResumeAgent. |
| **ResumeAgent** | Coordinator. Reads the request, identifies the section, delegates to the right specialist. |
| **SummaryAgent** | Reads and rewrites the professional summary. |
| **ExperienceAgent** | Adds, updates, or removes jobs and bullet points. |
| **SkillsAgent** | Adds or removes individual skills. |
| **ProjectsAgent** | Adds, updates, or removes project entries. |
| **EducationAgent** | Adds, updates, or removes education entries. |

**Flow of a typical request:**

1. You type something like *"Add Docker to my skills"*
2. **Unibot** receives it and passes it to **ResumeAgent**
3. **ResumeAgent** identifies this is a skills request → delegates to **SkillsAgent**
4. **SkillsAgent** calls `add_skill("Docker")` → saves to `resume.json`
5. You get a confirmation message

---

## Tool Reference

Each agent can only call specific tools. Here's the complete list:

### Read Tools (available to ResumeAgent)
| Tool | What it does |
|------|--------------|
| `get_resume()` | Returns the entire resume as JSON |
| `get_section(name)` | Returns one section: `summary`, `experiences`, `skills`, `projects`, or `education` |

### Summary Tools
| Tool | What it does |
|------|--------------|
| `get_summary()` | Returns the current summary text |
| `update_summary(text)` | Replaces the summary with new text |

### Experience Tools
| Tool | What it does |
|------|--------------|
| `get_experiences()` | Returns all experience entries |
| `get_experience_by_id(id)` | Returns one experience (e.g., `exp_1`) |
| `update_experience(id, ...)` | Updates company, role, or dates |
| `add_experience(company, role, dates)` | Adds a new job entry |
| `remove_experience(id)` | Deletes an experience entry |
| `add_bullet(id, text)` | Adds a bullet point to a job |
| `update_bullet(id, index, text)` | Updates a specific bullet (0-based index) |
| `remove_bullet(id, index)` | Removes a specific bullet |

### Skills Tools
| Tool | What it does |
|------|--------------|
| `get_skills()` | Returns all skills as a list |
| `add_skill(skill)` | Adds one skill (checks for duplicates) |
| `remove_skill(skill)` | Removes a skill by exact name |

### Projects Tools
| Tool | What it does |
|------|--------------|
| `get_projects()` | Returns all projects |
| `get_project_by_id(id)` | Returns one project (e.g., `proj_1`) |
| `add_project(name, description)` | Adds a new project |
| `update_project(id, ...)` | Updates name or description |
| `remove_project(id)` | Deletes a project |

### Education Tools
| Tool | What it does |
|------|--------------|
| `get_education()` | Returns all education entries |
| `get_education_by_id(id)` | Returns one entry (e.g., `edu_1`) |
| `update_education(id, ...)` | Updates degree, institution, or year |
| `add_education(degree, institution, year)` | Adds a new education entry |
| `remove_education(id)` | Deletes an education entry |

---

## Data Schema

Your resume is stored in `resume.json`. The structure follows this schema (validated by Pydantic):

```json
{
  "summary": "Your professional summary text here",

  "experiences": [
    {
      "id": "exp_1",
      "company": "Company Name",
      "role": "Job Title",
      "dates": "Jan 2023 – Present",
      "bullets": [
        "Bullet point one",
        "Bullet point two"
      ]
    }
  ],

  "skills": ["Python", "Docker", "Kubernetes"],

  "projects": [
    {
      "id": "proj_1",
      "name": "Project Name",
      "description": "What the project does"
    }
  ],

  "education": [
    {
      "id": "edu_1",
      "degree": "B.Tech in Computer Science",
      "institution": "University Name",
      "year": "2021 – 2025"
    }
  ]
}
```

> **To personalize**: Edit `resume.json` directly with your own data before starting the app.

Every time an agent saves a change, it validates the full file against this schema. If something is wrong, it throws an error — your data is never silently corrupted.

---

## Performance Metrics

Since the app uses Gemini API (cloud-based), there's no local model loading. Typical response times:

| Operation | Expected Time |
|-----------|---------------|
| Simple question / greeting | < 2 seconds |
| Reading a section | 1–3 seconds |
| Single tool call (add/remove) | 2–4 seconds |
| Multi-step operation | 4–8 seconds |

> Times depend on your internet connection and current Gemini API load.

**Requirements:**
- Python 3.11+
- ~100MB disk space (no large model files)
- Internet connection (for Gemini API calls)
- Free Gemini API key (generous free tier available)

---

## Troubleshooting

**`GOOGLE_API_KEY` not set or invalid**

```
Error: GOOGLE_API_KEY environment variable not found
```
→ Make sure you created `.env` from `.env.example` and filled in your actual key.

---

**`ModuleNotFoundError` when running**

```
ModuleNotFoundError: No module named 'google.adk'
```
→ Your virtual environment isn't active. Run:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

**Agent doesn't respond / times out**

→ Check your internet connection. Also verify your API key works at [aistudio.google.com](https://aistudio.google.com).

---

**Schema validation error after editing `resume.json`**

```
pydantic_core.ValidationError: 1 validation error for Resume
```
→ You have a structural error in `resume.json`. Check that all required fields (`id`, `company`, `role`, etc.) are present and correctly spelled.

---

**Wrong agent selected**

→ In the ADK web UI, make sure you select **unibot** (not one of the specialist agents) from the dropdown. Unibot is the entry point.

---

## Development

### Project Structure

```
resume_agent/
├── agents/
│   ├── unibot.py           # Entry point agent
│   ├── resume_agent.py     # Coordinator agent
│   ├── summary_agent.py    # Edits professional summary
│   ├── experience_agent.py # Edits work experiences
│   ├── skills_agent.py     # Manages skills list
│   ├── projects_agent.py   # Manages projects
│   └── education_agent.py  # Manages education entries
├── tools.py                # All read/write tool functions
├── schema.py               # Pydantic data models
├── resume.json             # Resume data file
├── requirements.txt        # Python dependencies
├── .env                    # Your API key (not committed)
└── .env.example            # Template for .env
```

### Adding a New Agent

1. Create a new file in `agents/` (e.g., `certifications_agent.py`)
2. Define the agent using `Agent(name=..., model="gemini-2.0-flash", tools=[...])`
3. Add it as a sub-agent in `resume_agent.py`
4. Add any new tool functions to `tools.py`
5. Update the Pydantic schema in `schema.py` if needed

### Adding a New Tool

```python
# In tools.py
def get_certifications() -> str:
    """Returns all certifications from the resume."""
    data = _load_resume()
    return json.dumps(data.get("certifications", []), indent=2)
```

Then pass it to the relevant agent's `tools=[...]` list.

### Running a Quick Test

```bash
# Check all agents load without errors
python3 -c "from agents.unibot import unibot; print('OK:', unibot.name)"

# Check a tool works
python3 -c "from tools import get_skills; print(get_skills())"

# Validate the current resume.json
python3 -c "from schema import Resume; import json; Resume(**json.load(open('resume.json'))); print('Schema OK')"
```

---

## Design Principles

ResumeForge was built around a few core ideas:

**1. One agent, one job**
Each specialist agent only touches one section of the resume. The skills agent never edits the summary. This makes the system predictable and easy to debug.

**2. Tools over memory**
Agents never rely on what they "remember" about the resume. Every read and write goes through a tool call. This eliminates hallucinations.

**3. Validate before saving**
Every time a change is made, the full `resume.json` is validated with Pydantic before being written to disk. Bad data never gets saved.

**4. Minimal changes**
Agents are instructed to only change what was specifically requested — not to rewrite the whole section or "improve" things you didn't ask about.

**5. Clear routing**
The coordinator agent (ResumeAgent) reads the user's request and routes it to the right specialist. No guessing, no ambiguity — if it's unclear, it asks.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**ResumeForge** — Professional resume editing through intelligent agent orchestration
