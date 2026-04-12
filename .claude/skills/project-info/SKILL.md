---
name: project-info
description: "Obtains detailed project information including framework, architecture, technologies, patterns, and dependencies. USE FOR: Identifying the tech stack, checking dependency versions, understanding the system architecture, and finding established patterns in the codebase. DO NOT USE FOR: Modifying the code or running development servers. INVOKES: list_dir, view_file, grep_search."
---

# Project Info Skill

This skill provides a systematic way to analyze the current project's structure, technologies, and dependencies.

## Information to Extract

When this skill is invoked, the goal is to identify:
1. **Framework & Orchestration**: Main frameworks used (e.g., .NET Aspire, Next.js, FastAPI).
2. **Architecture**: System design (e.g., Microservices, Monolith, Gateway-based).
3. **Technologies**: Core languages and tools (e.g., C#, Python, TypeScript, React, Vite).
4. **Patterns**: Established design patterns (e.g., Service Discovery, Reverse Proxy, Observability, CQRS).
5. **Dependencies**: Key libraries and their versions from relevant manifest files.

## Systematic Analysis Steps

### 1. Root Analysis (Orchestration & Global Config)
Check the root directory for orchestration files:
- `.NET Aspire`: `apphost.cs`, `aspire.config.json`.
- `Docker`: `docker-compose.yml`, `Dockerfile`.
- `JavaScript/TypeScript`: `package.json`, `lerna.json`, `pnpm-workspace.yaml`.
- `Python`: `pyproject.toml`, `requirements.txt`.

### 2. Services Analysis
Explore the `services/` or `apps/` directory to identify backend components:
- Check `pyproject.toml` or `requirements.txt` for Python services.
- Check `.csproj` for .NET services.
- Inspect `main.py`, `program.cs`, or `app.ts` to identify the framework (FastAPI, Express, etc.).

### 3. Frontend Analysis
Explore the `frontend/` or `client/` directory:
- Check `package.json` for framework (React, Vue, Angular) and version.
- Check `vite.config.ts`, `next.config.js`, or `webpack.config.js`.
- Check `src/` structure to identify state management or routing strategies.

### 4. Dependency Versions
Extract versions from:
- `package.json` (`dependencies` and `devDependencies`).
- `pyproject.toml` or `uv.lock`.
- `.csproj` files or `Directory.Packages.props`.

## Template for Reporting
When summarizing the project info, use this format:

```markdown
# Project Information Summary

## 🛠️ Framework & Orchestration
- **Main Framework**: [e.g. .NET Aspire 13.2]
- **Orchestrator**: [e.g. Aspire AppHost]

## 🏗️ Architecture & Patterns
- **Architecture**: [e.g. Microservices with YARP Gateway]
- **Key Patterns**: [e.g. Service Discovery, OTLP Tracing, Health Checks]

## 💻 Technologies
- **Languages**: [e.g. C#, Python 3.13, TypeScript]
- **Backend**: [e.g. FastAPI with Uvicorn]
- **Frontend**: [e.g. React 19 with Vite]

## 📦 Dependencies & Versions
### Backend (e.g. Weather Service)
- `fastapi`: [version]
- `opentelemetry`: [version]

### Frontend
- `react`: [version]
- `react-router-dom`: [version]
- `vite`: [version]
```
