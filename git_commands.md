# Git Commands to Push to GitHub

## Initial Setup (First Time Only)

```bash
# 1. Configure Git with your details (if not already done)
git config --global user.name "SkandaBR"
git config --global user.email "skanda.ramamurthy@gmail.com"

# 2. Add all files to staging
git add .

# 3. Create initial commit
git commit -m "Initial commit: MCP RAG & Calculator intelligent agent"

# 4. Add remote repository
git remote add origin https://github.com/SkandaBR/cal_rag_mcp_agent.git

# 5. Push to GitHub (first time - creates main branch)
git push -u origin main
```

---

## Regular Updates (After Initial Setup)

```bash
# 1. Check status of changes
git status

# 2. Add all changed files
git add .

# 3. Commit with a message
git commit -m "Your commit message here"

# 4. Push to GitHub
git push
```

---

## Useful Commands

```bash
# View commit history
git log --oneline

# View current branch
git branch

# View remote repository URL
git remote -v

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# Pull latest changes from GitHub
git pull

# Create and switch to new branch
git checkout -b feature-branch-name

# Switch back to main branch
git checkout main
```

---

## Common Scenarios

### Scenario 1: First Push to Empty GitHub Repository
```bash
git add .
git commit -m "Initial commit: MCP RAG & Calculator intelligent agent"
git remote add origin https://github.com/SkandaBR/cal_rag_mcp_agent.git
git push -u origin main
```

### Scenario 2: GitHub Repository Already Has Content
```bash
# Pull existing content first
git pull origin main --allow-unrelated-histories

# Then add and push your changes
git add .
git commit -m "Add MCP intelligent agent implementation"
git push origin main
```

### Scenario 3: Update Existing Repository
```bash
git add .
git commit -m "Update: [describe your changes]"
git push
```

---

## Commit Message Examples

Good commit messages are descriptive:

```bash
git commit -m "Add intelligent agent with context-based tool selection"
git commit -m "Fix: Calculator pattern matching for complex expressions"
git commit -m "Update: Improve UI with chat interface and tool badges"
git commit -m "Docs: Add flow.md with call hierarchy explanation"
git commit -m "Refactor: Simplify RAG retrieval logic"
```

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
# Remove existing remote and add again
git remote remove origin
git remote add origin https://github.com/SkandaBR/cal_rag_mcp_agent.git
```

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### Error: Authentication failed
```bash
# Use GitHub Personal Access Token instead of password
# Generate token at: https://github.com/settings/tokens
# Use token as password when prompted
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `git status` | Show current changes |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Commit with message |
| `git push` | Push to GitHub |
| `git pull` | Pull from GitHub |
| `git log` | View commit history |
| `git diff` | Show changes |
| `git branch` | List branches |
