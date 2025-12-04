# Reasoning Optimizer Skill

Enhance AI reasoning through structured frameworks and systematic thought processes. Use this skill when tackling complex tasks that require careful analysis, multi-step problem-solving, or high-quality code generation.

## When to Use This Skill

Invoke this skill when:
- Tasks require multi-step reasoning
- Code generation needs to be thorough and correct
- Complex analysis is needed
- High accuracy is critical
- Problems need systematic decomposition

## The 5-Phase Reasoning Model

Apply these phases to every complex task:

### Phase 1: Comprehension
- What exactly is being asked?
- What are the explicit and implicit requirements?
- What are the inputs and expected outputs?
- Are there any constraints or limitations?
- Can I restate this problem clearly?

### Phase 2: Strategy
- What are the possible approaches?
- What patterns or algorithms apply?
- What are the trade-offs of each approach?
- What is the optimal approach given requirements?
- What could go wrong?

### Phase 3: Execution
- Follow the planned steps
- Ensure each step connects logically
- Document reasoning as you go
- Produce initial output

### Phase 4: Review
- Does output address ALL requirements?
- Are edge cases covered?
- Is logic sound and consistent?
- Are there errors or mistakes?
- Would this satisfy the request?

### Phase 5: Refinement
- Address identified issues
- Optimize where possible
- Polish the output
- Final verification

## Chain-of-Thought Template

```markdown
## Problem Understanding
[Restate the problem]

## Known Information
- [Fact 1]
- [Fact 2]

## Reasoning Steps

### Step 1: [Description]
[Work] → Result: [Intermediate result]

### Step 2: [Description]
[Work] → Result: [Intermediate result]

## Conclusion
[Final answer with justification]
```

## Code Generation Process

### Step 1: Understand
- What should the code do?
- What are inputs/outputs?
- What are constraints?

### Step 2: Plan
- Choose algorithm/approach
- Select data structures
- Identify edge cases
- Plan error handling

### Step 3: Construct
- Write code segment by segment
- Keep it clean and readable
- Comment significant decisions

### Step 4: Review
- Check against requirements
- Verify edge case handling
- Look for security issues

### Step 5: Refine
- Fix identified issues
- Optimize if needed
- Polish the code

## Quality Checklists

### Pre-Response Check
- [ ] I understand what is being asked
- [ ] I have a plan for approaching this
- [ ] I know the expected output format

### Post-Response Check
- [ ] Response addresses the actual question
- [ ] All parts of the request are covered
- [ ] Reasoning is sound and logical
- [ ] Edge cases are considered
- [ ] Quality meets expectations

### Code Quality Check
- [ ] Code runs without errors
- [ ] Correct output for normal inputs
- [ ] Edge cases handled
- [ ] Readable and well-formatted
- [ ] No security vulnerabilities
- [ ] Appropriate error handling

## Self-Correction Protocol

After generating a solution:

1. **Accuracy**: Is this correct? Any logical errors?
2. **Completeness**: All requirements addressed?
3. **Quality**: Is this the best approach?
4. **Confidence**: Am I satisfied with this?

If issues found → Revise and repeat

## Depth Calibration

| Task Complexity | Approach |
|-----------------|----------|
| Simple | Light check, direct answer |
| Moderate | Standard phases, basic checklist |
| Complex | Full 5-phase, detailed checklists |
| Critical | Maximum depth, multiple verification |

## Reasoning Patterns

- **Divide and Conquer**: Break large problems into sub-problems
- **Working Backwards**: Start from goal, trace back to start
- **Constraint Satisfaction**: Check all constraints are met
- **Iterative Refinement**: Generate → Evaluate → Improve → Repeat
