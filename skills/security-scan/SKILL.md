---
name: security-scan
description: Security scan of the project — findings by severity with file:line and remediation.
whenToUse: Before merging a PR that touches auth or user input, or when the user asks for a security review
---

# Security Scan

Run a focused security scan of the current project.

First, gather context with Bash:
- Current directory: `pwd`
- Recent changes: `git diff HEAD --name-only 2>/dev/null | head -20`
- Package dependencies: `cat package.json 2>/dev/null || cat requirements.txt 2>/dev/null | head -20`

Then delegate to a `coder` subagent (read-only — no edits). Brief it with:
1. The project directory and recent changes (prioritise scanning these files first)
2. The checklist below

Scan for:
- User input passed to shell commands without sanitisation
- SQL built via string concatenation
- Hardcoded secrets or credentials
- Missing auth checks on protected routes/functions
- Injection, XSS, CSRF, path traversal, unsafe deserialization
- Dependency red flags in the package manifest

Output contract: `VULN: [HIGH] file:line — description — remediation`, or "No findings".

After the scan completes, present:
- Total findings by severity (HIGH / MED / LOW)
- Each HIGH finding with file path, line number, description, and remediation
- MED/LOW findings summarised
- "No findings" if clean
