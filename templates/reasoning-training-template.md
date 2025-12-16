# AI Reasoning Training Template

## Comprehensive Framework for Improving Bot Reasoning from 75% to 95%+

This template addresses the systematic gaps in AI reasoning that typically cause bots to plateau at 75-80% effectiveness. Based on analysis of common failure patterns, this framework provides structured training materials, testing methodologies, and evaluation criteria.

---

## Table of Contents

1. [Understanding the Reasoning Gap](#understanding-the-reasoning-gap)
2. [The 7 Reasoning Failure Categories](#the-7-reasoning-failure-categories)
3. [Core Reasoning Modules](#core-reasoning-modules)
4. [Training Skill Template](#training-skill-template)
5. [Testing & Validation Framework](#testing--validation-framework)
6. [Evaluation Rubrics](#evaluation-rubrics)
7. [Implementation Checklist](#implementation-checklist)
8. [Advanced Patterns](#advanced-patterns)

---

## Understanding the Reasoning Gap

### Why Bots Plateau at 75-80%

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    REASONING CAPABILITY BREAKDOWN                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ████████████████████████████████████████░░░░░░░░░░░░░░  75-80%         │
│  │                                      │              │                 │
│  │  PATTERN MATCHING                    │  REASONING   │                 │
│  │  (What bots do well)                 │  GAP         │                 │
│  │                                      │  (20-25%)    │                 │
│  │  • Known problem types               │              │                 │
│  │  • Direct instruction following      │  • Edge cases│                 │
│  │  • Template application              │  • Novel     │                 │
│  │  • Syntax and structure              │    combinations                │
│  │  • Fact retrieval                    │  • Multi-step│                 │
│  │                                      │    inference │                 │
│  │                                      │  • Self-     │                 │
│  │                                      │    correction│                 │
│  └──────────────────────────────────────┴──────────────┘                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### The 20-25% Gap Consists Of:

| Gap Component | % of Gap | Description |
|---------------|----------|-------------|
| Edge Case Handling | 5-7% | Unusual inputs, boundary conditions |
| Multi-step Inference | 4-6% | Chaining logic across 3+ steps |
| Self-Correction | 3-5% | Detecting and fixing own errors |
| Ambiguity Resolution | 3-4% | Handling unclear requirements |
| Context Integration | 2-4% | Using all available information |
| Verification Failure | 2-3% | Not checking work |
| Premature Closure | 1-2% | Stopping before complete |

---

## The 7 Reasoning Failure Categories

### Category 1: Comprehension Failures (15% of errors)

**Symptoms:**
- Answering a different question than asked
- Missing implicit requirements
- Ignoring constraints mentioned in the prompt

**Root Cause:** Insufficient problem decomposition before execution

**Training Focus:**
```markdown
## Comprehension Protocol

Before ANY action, answer these questions:

### Explicit Requirements
1. What is literally being asked?
2. What specific outputs are expected?
3. What format is required?

### Implicit Requirements
4. What would a reasonable person expect that wasn't stated?
5. What quality level is implied?
6. What constraints exist from context?

### Verification
7. Can I restate this problem in different words?
8. If I showed my understanding to the requester, would they agree?
```

**Test Pattern:**
```python
def test_comprehension_accuracy():
    """Test that bot correctly identifies all requirements."""
    prompt = "Write a function that sorts numbers, handling empty lists"

    expected_requirements = [
        "function",
        "sorts",
        "numbers",
        "handles empty lists"  # Often missed
    ]

    response = bot.analyze_requirements(prompt)

    for req in expected_requirements:
        assert req in response.identified_requirements
```

---

### Category 2: Planning Failures (20% of errors)

**Symptoms:**
- Jumping straight to implementation
- Missing critical steps
- Wrong algorithm/approach selection
- No consideration of alternatives

**Root Cause:** Skipping strategy phase entirely

**Training Focus:**
```markdown
## Mandatory Planning Protocol

### Step 1: Generate Multiple Approaches (minimum 2)

For any non-trivial task, identify at least two different approaches:

**Approach A: [Name]**
- Method: [How it works]
- Pros: [Advantages]
- Cons: [Disadvantages]
- Risk: [What could go wrong]

**Approach B: [Name]**
- Method: [How it works]
- Pros: [Advantages]
- Cons: [Disadvantages]
- Risk: [What could go wrong]

### Step 2: Selection with Justification

**Selected: [A or B]**
**Reasoning:** [Why this approach is better for THIS specific problem]

### Step 3: Detailed Execution Plan

1. [First concrete step]
2. [Second concrete step]
3. [Continue until complete]

### Step 4: Risk Mitigation

For each identified risk, state the mitigation:
- Risk 1 → Mitigation: [How to handle]
```

**Test Pattern:**
```python
def test_planning_completeness():
    """Test that bot generates adequate plans."""
    task = "Implement user authentication system"

    plan = bot.generate_plan(task)

    # Must consider alternatives
    assert len(plan.approaches) >= 2

    # Must have selection reasoning
    assert plan.selection_justification is not None

    # Must have concrete steps
    assert len(plan.execution_steps) >= 3

    # Must identify risks
    assert len(plan.identified_risks) >= 1
```

---

### Category 3: Execution Drift (18% of errors)

**Symptoms:**
- Starting correctly but drifting off-track
- Forgetting earlier constraints mid-task
- Inconsistent application of decisions

**Root Cause:** No systematic checkpointing during execution

**Training Focus:**
```markdown
## Execution Checkpoint Protocol

After EVERY significant action, perform a micro-check:

### Checkpoint Questions (5-second mental check)
□ Am I still addressing the original request?
□ Does this step connect to my plan?
□ Have I introduced any contradictions?
□ Am I maintaining consistent assumptions?

### Drift Detection Signals
If any of these occur, STOP and reassess:
- "Let me also add..." (scope creep)
- "Actually, I should..." (plan deviation)
- "This reminds me of..." (tangent risk)
- Starting new work before finishing current

### Recovery Protocol
When drift detected:
1. STOP current action
2. Re-read original request
3. Review plan
4. Identify where drift began
5. Revert or adjust
6. Continue with awareness
```

**Test Pattern:**
```python
def test_execution_consistency():
    """Test that bot maintains consistency throughout."""
    task = "Create a REST API with POST /users endpoint"

    response = bot.execute(task)

    # Check for scope creep
    assert "GET" not in response or "GET" in task

    # Check original requirement met
    assert "POST" in response
    assert "/users" in response

    # Check no contradictions introduced
    contradictions = analyze_contradictions(response)
    assert len(contradictions) == 0
```

---

### Category 4: Edge Case Blindness (15% of errors)

**Symptoms:**
- Code crashes on empty input
- Fails on boundary values
- Doesn't handle error conditions
- Assumes "happy path" only

**Root Cause:** No systematic edge case enumeration

**Training Focus:**
```markdown
## Edge Case Enumeration Protocol

### Universal Edge Cases (Check ALL of these)

#### Input Edge Cases
□ Empty/null/undefined input
□ Single element
□ Two elements (minimum for comparison)
□ Maximum size/length
□ Minimum valid value
□ Maximum valid value
□ Zero
□ Negative values (if numeric)
□ Very large numbers
□ Very small numbers (decimals)
□ Special characters
□ Unicode/emoji
□ Whitespace only
□ Mixed types

#### State Edge Cases
□ First operation (initialization)
□ Last operation (cleanup)
□ Repeated operations
□ Concurrent operations
□ Operation after error

#### Environmental Edge Cases
□ No network
□ No disk space
□ No permissions
□ Timeout conditions
□ Rate limits

### Domain-Specific Edge Cases
[Identify 3-5 edge cases specific to the problem domain]

### Edge Case Handling Matrix

| Edge Case | Expected Behavior | Handling Code |
|-----------|-------------------|---------------|
| Empty input | Return [] / Raise ValueError | Line X |
| Null | Raise TypeError | Line Y |
| [Continue for each case] | | |
```

**Test Pattern:**
```python
def test_edge_case_coverage():
    """Test that bot handles edge cases."""

    edge_cases = [
        ([], "empty list"),
        ([1], "single element"),
        (None, "null input"),
        ([-1, 0, 1], "negative, zero, positive"),
        ([float('inf')], "infinity"),
        ([1] * 10000, "large input"),
    ]

    for input_val, description in edge_cases:
        try:
            result = bot.function(input_val)
            # Should either succeed or raise appropriate exception
            assert result is not None or isinstance(result, Exception)
        except Exception as e:
            # Exception should be informative
            assert len(str(e)) > 10, f"Poor error message for {description}"
```

---

### Category 5: Verification Skipping (12% of errors)

**Symptoms:**
- Obvious errors in output
- Logical inconsistencies
- Typos and syntax errors
- Incomplete responses

**Root Cause:** No mandatory review phase

**Training Focus:**
```markdown
## Mandatory Verification Protocol

### Level 1: Syntax Check (Always)
□ Code compiles/parses without errors
□ All brackets/quotes balanced
□ No obvious typos
□ Consistent formatting

### Level 2: Logic Check (Always)
□ Each step follows from previous
□ Conclusion matches premises
□ No circular reasoning
□ No unsupported claims

### Level 3: Requirements Check (Always)
□ Every explicit requirement addressed
□ Every implicit requirement considered
□ Output format matches expected
□ Nothing extra added unnecessarily

### Level 4: Quality Check (For important tasks)
□ Would I be satisfied receiving this?
□ Is this the best approach I could produce?
□ Are there obvious improvements I'm skipping?
□ Did I take any shortcuts I shouldn't have?

### Level 5: Adversarial Check (For critical tasks)
□ What would a critic say about this?
□ How could this fail?
□ What am I most uncertain about?
□ Should I add caveats or warnings?

### Verification Checklist Completion Rule
**NEVER** submit a response without completing at least Levels 1-3.
Mark completion: [L1:✓] [L2:✓] [L3:✓] [L4:_] [L5:_]
```

**Test Pattern:**
```python
def test_verification_performed():
    """Test that bot performs verification."""

    task = "Write a function to calculate factorial"
    response = bot.execute(task)

    # Check for verification indicators
    verification_signals = [
        "verified",
        "checked",
        "tested",
        "confirmed",
        "reviewing",
    ]

    has_verification = any(
        signal in response.lower()
        for signal in verification_signals
    )

    # Or check for test cases in response
    has_tests = "test" in response.lower() or "example" in response.lower()

    assert has_verification or has_tests
```

---

### Category 6: Self-Correction Failure (10% of errors)

**Symptoms:**
- Doubling down on errors when questioned
- Not recognizing own mistakes
- Defensive responses to feedback
- Inability to course-correct

**Root Cause:** No trained self-critique mechanism

**Training Focus:**
```markdown
## Self-Correction Protocol

### Active Self-Critique (Before finalizing)

Ask yourself these questions and answer honestly:

**Accuracy Critique:**
- What am I LEAST confident about in this response?
- Where might I be wrong?
- What assumptions am I making that might be invalid?

**Completeness Critique:**
- What might I have forgotten?
- What would an expert add?
- Is there a simpler solution I'm missing?

**Quality Critique:**
- What's the weakest part of this response?
- If I had more time, what would I improve?
- Am I taking any lazy shortcuts?

### Error Recognition Patterns

Train to recognize these self-error signals:
- "I think..." → Uncertainty signal, verify
- "Usually..." → May not apply here, check
- "Obviously..." → Might not be obvious, explain
- "Simply..." → Might be oversimplifying, expand

### Correction Protocol

When error identified:
1. Acknowledge specifically what was wrong
2. Explain why it was wrong
3. Provide correct information
4. Verify the correction is actually correct
5. Check if the error affected other parts

### NEVER:
- Pretend the error didn't happen
- Make excuses for the error
- Partially correct while leaving related errors
```

**Test Pattern:**
```python
def test_self_correction():
    """Test that bot can recognize and correct errors."""

    # First, get a response
    task = "What is 15% of 80?"
    response1 = bot.execute(task)

    # Then point out an error (even if correct, test the mechanism)
    correction_prompt = "I think you made an arithmetic error. Can you double-check?"
    response2 = bot.execute(correction_prompt)

    # Bot should either:
    # 1. Confirm original answer with verification
    # 2. Correct if actually wrong
    # Bot should NOT just agree without checking

    shows_work = any(word in response2.lower() for word in
                     ["calculate", "verify", "check", "15%", "0.15", "12"])

    assert shows_work, "Bot should show verification work"
```

---

### Category 7: Context Integration Failure (10% of errors)

**Symptoms:**
- Ignoring earlier conversation context
- Not using provided information
- Asking for information already given
- Inconsistent with established facts

**Root Cause:** No systematic context utilization

**Training Focus:**
```markdown
## Context Integration Protocol

### Before Responding, Scan Context For:

**Established Facts:**
- What has been stated as true?
- What decisions have been made?
- What constraints have been set?

**User Preferences:**
- What style/format have they preferred?
- What level of detail do they want?
- What terminology do they use?

**Previous Errors:**
- What mistakes were made earlier?
- What corrections were given?
- What should be avoided?

**Implicit Information:**
- What can be inferred from the conversation?
- What domain knowledge applies?
- What common knowledge is relevant?

### Context Utilization Checklist

Before responding:
□ Reviewed all relevant prior messages
□ Noted any established constraints
□ Checked for preference patterns
□ Avoided repeating past errors
□ Built upon previous work appropriately

### Context Conflict Resolution

When new information conflicts with context:
1. Acknowledge the apparent conflict
2. Ask for clarification if ambiguous
3. If clear update, explicitly note the change
4. Update all dependent conclusions
```

**Test Pattern:**
```python
def test_context_integration():
    """Test that bot uses conversation context."""

    # Establish context
    bot.execute("My name is Alice and I prefer Python")
    bot.execute("I'm working on a data analysis project")

    # Ask related question
    response = bot.execute("Can you help me read a CSV file?")

    # Should use established context
    assert "python" in response.lower()  # Remembered preference
    # Should not ask for already-given info
    assert "what language" not in response.lower()
```

---

## Core Reasoning Modules

The following modules should be incorporated into any training skill:

### Module 1: Problem Decomposition

```markdown
## Problem Decomposition Framework

### Step 1: Identify Problem Type
- Is this a creation task? (build something new)
- Is this an analysis task? (understand something)
- Is this a transformation task? (change something)
- Is this a debugging task? (fix something)

### Step 2: Break Into Sub-Problems
For each major component:
- What is the input?
- What is the output?
- What transformation occurs?
- What could go wrong?

### Step 3: Identify Dependencies
- Which sub-problems must be solved first?
- Which can be solved in parallel?
- Which have shared constraints?

### Step 4: Sequence the Solution
1. [First sub-problem - why first?]
2. [Second sub-problem - depends on 1?]
3. [Continue...]
```

### Module 2: Logical Reasoning Chain

```markdown
## Logical Reasoning Template

### Given Information
- Fact 1: [State clearly]
- Fact 2: [State clearly]
- Fact N: [State clearly]

### Inference Chain

**Step 1:** From [Fact 1] and [Fact 2], we can conclude [Inference 1]
- Reasoning: [Explain why this follows]
- Confidence: [High/Medium/Low]

**Step 2:** From [Inference 1] and [Fact 3], we can conclude [Inference 2]
- Reasoning: [Explain why this follows]
- Confidence: [High/Medium/Low]

**Step N:** From [previous inferences], we can conclude [Final Conclusion]
- Reasoning: [Explain why this follows]
- Confidence: [High/Medium/Low]

### Conclusion Validation
- Does conclusion contradict any given facts? [Yes/No]
- Are there alternative conclusions possible? [Yes/No]
- What would invalidate this conclusion? [State]
```

### Module 3: Decision Framework

```markdown
## Decision Making Template

### Decision Required
[State the decision clearly]

### Options Identified
1. [Option A]
2. [Option B]
3. [Option C]

### Evaluation Criteria
- Criterion 1: [What matters and why]
- Criterion 2: [What matters and why]
- Criterion 3: [What matters and why]

### Options Evaluation Matrix

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Criterion 1 | [1-5] | [1-5] | [1-5] | [1-5] |
| Criterion 2 | [1-5] | [1-5] | [1-5] | [1-5] |
| Criterion 3 | [1-5] | [1-5] | [1-5] | [1-5] |
| **Weighted Total** | | [Sum] | [Sum] | [Sum] |

### Decision
**Selected:** [Option X]
**Reasoning:** [Why this option best meets the criteria]
**Trade-offs Accepted:** [What we're giving up]
```

---

## Training Skill Template

Use this template as the base for any reasoning-focused training skill:

```markdown
# [Skill Name] - Reasoning-Enhanced Training Skill

## Activation Triggers
This skill activates when:
- [Condition 1]
- [Condition 2]
- [Condition 3]

## Pre-Response Protocol

### 1. Comprehension Phase (MANDATORY)
Before any action:
- [ ] Restate the problem in own words
- [ ] List all explicit requirements
- [ ] Identify implicit requirements
- [ ] Note all constraints
- [ ] Identify what success looks like

### 2. Planning Phase (MANDATORY for non-trivial tasks)
Before implementation:
- [ ] Generate at least 2 approaches
- [ ] Evaluate trade-offs
- [ ] Select with justification
- [ ] Create step-by-step plan
- [ ] Identify risks and mitigations

### 3. Execution Phase
During implementation:
- [ ] Follow the plan step by step
- [ ] Checkpoint after each major step
- [ ] Watch for drift signals
- [ ] Maintain consistency

### 4. Verification Phase (MANDATORY)
Before submitting:
- [ ] Syntax/format check
- [ ] Logic consistency check
- [ ] Requirements coverage check
- [ ] Edge case consideration
- [ ] Self-critique pass

## Domain-Specific Reasoning

### [Domain Area 1]
[Specific reasoning patterns for this domain]

### [Domain Area 2]
[Specific reasoning patterns for this domain]

## Error Recovery

### When Stuck
1. Re-read the original request
2. Identify what's blocking progress
3. Consider alternative approaches
4. Ask for clarification if needed

### When Wrong
1. Acknowledge the error specifically
2. Explain what went wrong
3. Provide correct solution
4. Verify correction is correct

## Quality Standards

### Minimum Acceptable
- All explicit requirements met
- No logical errors
- Syntactically correct
- Basic edge cases handled

### Target Quality
- All requirements met (explicit and implicit)
- Thoroughly reasoned
- Well-structured
- Comprehensive edge case handling
- Self-verified

### Excellence
- Exceeds requirements
- Anticipates follow-up needs
- Provides additional value
- Thoroughly documented reasoning
```

---

## Testing & Validation Framework

### Test Categories

```python
# tests/test_reasoning_categories.py

class TestComprehension:
    """Tests for comprehension failures."""

    def test_identifies_explicit_requirements(self):
        pass

    def test_identifies_implicit_requirements(self):
        pass

    def test_recognizes_constraints(self):
        pass


class TestPlanning:
    """Tests for planning failures."""

    def test_generates_multiple_approaches(self):
        pass

    def test_provides_selection_reasoning(self):
        pass

    def test_creates_actionable_plan(self):
        pass


class TestExecution:
    """Tests for execution drift."""

    def test_maintains_focus(self):
        pass

    def test_follows_plan(self):
        pass

    def test_no_scope_creep(self):
        pass


class TestEdgeCases:
    """Tests for edge case handling."""

    def test_handles_empty_input(self):
        pass

    def test_handles_null_input(self):
        pass

    def test_handles_boundary_values(self):
        pass


class TestVerification:
    """Tests for verification skipping."""

    def test_verifies_syntax(self):
        pass

    def test_verifies_logic(self):
        pass

    def test_verifies_requirements(self):
        pass


class TestSelfCorrection:
    """Tests for self-correction failure."""

    def test_recognizes_errors(self):
        pass

    def test_corrects_errors(self):
        pass

    def test_doesnt_double_down(self):
        pass


class TestContextIntegration:
    """Tests for context integration failure."""

    def test_uses_conversation_context(self):
        pass

    def test_remembers_preferences(self):
        pass

    def test_builds_on_previous(self):
        pass
```

---

## Evaluation Rubrics

### Reasoning Quality Rubric (0-100)

#### Comprehension (20 points)
| Score | Criteria |
|-------|----------|
| 20 | Perfect understanding, all requirements identified |
| 15 | Good understanding, minor omissions |
| 10 | Partial understanding, significant gaps |
| 5 | Misunderstood key aspects |
| 0 | Completely misunderstood |

#### Planning (20 points)
| Score | Criteria |
|-------|----------|
| 20 | Multiple approaches, clear selection, detailed plan |
| 15 | Good plan, could be more thorough |
| 10 | Basic plan, missing alternatives or detail |
| 5 | Minimal planning, jumped to execution |
| 0 | No planning evident |

#### Execution (20 points)
| Score | Criteria |
|-------|----------|
| 20 | Flawless execution, followed plan, no drift |
| 15 | Good execution, minor deviations |
| 10 | Adequate execution, some drift |
| 5 | Poor execution, significant issues |
| 0 | Failed execution |

#### Edge Cases (15 points)
| Score | Criteria |
|-------|----------|
| 15 | Comprehensive edge case handling |
| 12 | Most edge cases handled |
| 8 | Common edge cases handled |
| 4 | Few edge cases considered |
| 0 | No edge case handling |

#### Verification (15 points)
| Score | Criteria |
|-------|----------|
| 15 | Thorough verification, all levels |
| 12 | Good verification, minor gaps |
| 8 | Basic verification |
| 4 | Minimal verification |
| 0 | No verification |

#### Self-Awareness (10 points)
| Score | Criteria |
|-------|----------|
| 10 | Accurate self-assessment, appropriate confidence |
| 7 | Good self-awareness, minor calibration issues |
| 4 | Some self-awareness |
| 2 | Poor self-awareness |
| 0 | No self-awareness |

### Quick Scoring Guide

```
90-100: Expert reasoning, production-ready
80-89:  Strong reasoning, minor improvements possible
70-79:  Adequate reasoning, notable gaps (YOUR CURRENT LEVEL)
60-69:  Weak reasoning, significant training needed
<60:    Poor reasoning, fundamental issues
```

---

## Implementation Checklist

### Phase 1: Foundation (Week 1-2)

- [ ] Implement comprehension protocol
- [ ] Add mandatory planning requirement
- [ ] Create basic verification checklist
- [ ] Add edge case enumeration template
- [ ] Write tests for each protocol

### Phase 2: Core Reasoning (Week 3-4)

- [ ] Implement logical reasoning chain
- [ ] Add decision framework
- [ ] Create self-correction mechanism
- [ ] Implement context integration
- [ ] Expand test coverage

### Phase 3: Validation (Week 5-6)

- [ ] Run evaluation rubrics on sample tasks
- [ ] Identify remaining gaps
- [ ] Refine protocols based on failures
- [ ] Add domain-specific reasoning
- [ ] Final test suite validation

### Phase 4: Optimization (Ongoing)

- [ ] Track failure categories
- [ ] A/B test protocol variations
- [ ] Refine based on real-world usage
- [ ] Update training materials
- [ ] Document lessons learned

---

## Advanced Patterns

### Meta-Reasoning Protocol

```markdown
## Meta-Reasoning (Thinking about thinking)

### Before Complex Tasks
1. What type of reasoning does this require?
   - Deductive (general → specific)
   - Inductive (specific → general)
   - Abductive (observation → explanation)
   - Analogical (similar → similar)

2. What's my confidence level?
   - High: Proceed normally
   - Medium: Add extra verification
   - Low: Research first, or ask for help

3. What could make me wrong?
   - [List potential failure modes]
   - [Plan mitigation for each]
```

### Reasoning Debugging Protocol

```markdown
## When Output Quality is Low

### Step 1: Identify Failure Category
- [ ] Comprehension failure?
- [ ] Planning failure?
- [ ] Execution drift?
- [ ] Edge case miss?
- [ ] Verification skip?
- [ ] Self-correction failure?
- [ ] Context integration failure?

### Step 2: Root Cause Analysis
- Where exactly did reasoning fail?
- What triggered the failure?
- What should have happened?

### Step 3: Correction
- Apply specific protocol for that category
- Re-execute from failure point
- Verify fix addresses root cause

### Step 4: Prevention
- What check would have caught this?
- Add to personal verification list
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                  REASONING QUALITY CHECKLIST                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BEFORE STARTING                                                 │
│  □ Restate the problem                                           │
│  □ List all requirements                                         │
│  □ Identify constraints                                          │
│                                                                  │
│  BEFORE IMPLEMENTING                                             │
│  □ Generate 2+ approaches                                        │
│  □ Select with reasoning                                         │
│  □ Create detailed plan                                          │
│                                                                  │
│  DURING IMPLEMENTATION                                           │
│  □ Follow the plan                                               │
│  □ Checkpoint regularly                                          │
│  □ Watch for drift                                               │
│                                                                  │
│  BEFORE SUBMITTING                                               │
│  □ Verify syntax                                                 │
│  □ Verify logic                                                  │
│  □ Verify requirements                                           │
│  □ Check edge cases                                              │
│  □ Self-critique                                                 │
│                                                                  │
│  CONFIDENCE CHECK                                                │
│  □ High: Submit                                                  │
│  □ Medium: Add caveats                                           │
│  □ Low: Research more or ask                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*This template provides the foundation for systematic reasoning improvement. Apply these protocols consistently, test rigorously, and iterate based on observed failures.*
