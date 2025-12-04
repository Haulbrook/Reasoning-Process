# Reasoning Optimizer Skill

A comprehensive AI reasoning enhancement skill for Claude Code that provides structured frameworks, checklists, and systematic thought processes for improved problem-solving.

## Overview

This skill enables Claude to enhance its reasoning capabilities through:

- **5-Phase Reasoning Model**: Comprehension → Strategy → Execution → Review → Refinement
- **Chain-of-Thought Frameworks**: Structured step-by-step reasoning
- **Code Generation Reasoning**: Specialized process for writing quality code
- **Checklists & Filters**: Verification systems for accuracy and completeness
- **Self-Correction Protocols**: Iterative improvement mechanisms

## Installation

### For Claude Code Users

Copy the skill file to your Claude Code skills directory:

```bash
# User-level installation (available in all projects)
cp skill.md ~/.claude/skills/reasoning-optimizer.md

# Project-level installation (available only in this project)
mkdir -p .claude/skills
cp skill.md .claude/skills/reasoning-optimizer.md
```

### Usage

Once installed, the skill can be invoked when you need enhanced reasoning capabilities:

1. **Automatic**: Claude will use these frameworks when tackling complex tasks
2. **Manual**: Reference the skill when you want explicit structured reasoning

## Key Components

### The 5-Phase Reasoning Model

1. **Comprehension**: Parse and understand the problem
2. **Strategy**: Brainstorm and plan the approach
3. **Execution**: Implement the solution step-by-step
4. **Review**: Verify against requirements
5. **Refinement**: Polish and finalize

### Chain-of-Thought (CoT)

Structured templates for showing reasoning work, particularly useful for:
- Mathematical problems
- Complex logic
- Multi-step analysis

### Code Generation Reasoning

A 5-step process specifically for code:
1. Understanding the problem
2. Planning the solution
3. Step-by-step construction
4. Documenting decisions
5. Iterative refinement

### Master Checklists

- Universal Pre-Response Checklist
- Universal Post-Response Checklist
- Code-Specific Quality Checklist
- Problem-Solving Checklist

## License

MIT License - Feel free to use, modify, and distribute.

## Contributing

Contributions welcome! Please submit issues and pull requests to improve the reasoning frameworks.
