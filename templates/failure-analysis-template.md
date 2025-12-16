# Reasoning Failure Analysis Template

Use this template to systematically analyze when your bot fails to reach 90%+ quality. Each failure should be documented and used to improve training.

---

## Failure Record

### Failure ID: [YYYY-MM-DD-###]

**Date:** [Date of failure]
**Task Type:** [Code / Analysis / Explanation / Problem-solving / Other]
**Complexity Level:** [Simple / Moderate / Complex / Critical]

---

## Input Analysis

### Original Prompt
```
[Paste the exact prompt that caused the failure]
```

### Expected Output
```
[What should have been produced]
```

### Actual Output
```
[What was actually produced]
```

---

## Failure Classification

### Primary Failure Category
Select ONE primary category:

- [ ] **Comprehension** - Misunderstood the request
- [ ] **Planning** - Poor or missing strategy
- [ ] **Execution Drift** - Started right, went wrong
- [ ] **Edge Case** - Missed boundary/special cases
- [ ] **Verification** - Didn't check work
- [ ] **Self-Correction** - Couldn't fix own error
- [ ] **Context Integration** - Ignored relevant context

### Secondary Failure Categories
Select any additional contributing factors:

- [ ] Comprehension
- [ ] Planning
- [ ] Execution Drift
- [ ] Edge Case
- [ ] Verification
- [ ] Self-Correction
- [ ] Context Integration

---

## Root Cause Analysis

### What Went Wrong?
[Detailed explanation of the failure]

### Where in the Process Did It Fail?
```
Comprehension → Planning → Execution → Verification → Output
      ↑
   [Mark where failure occurred]
```

### Why Did It Fail?
[Analysis of why this specific failure happened]

### What Should Have Happened?
[Step-by-step correct reasoning]

---

## Impact Assessment

### Severity Level
- [ ] **Critical** - Complete wrong answer, potential harm
- [ ] **Major** - Wrong answer, significant impact
- [ ] **Moderate** - Partially wrong, usable with fixes
- [ ] **Minor** - Small issues, mostly correct

### User Impact
[How this failure affected the user]

### Pattern Recognition
Is this a recurring failure?
- [ ] First occurrence
- [ ] Seen before (# times: ___)
- [ ] Known weakness area

---

## Correction Protocol

### Immediate Fix
[What should be done to fix this specific instance]

### Training Improvement
[What should be added to training to prevent this]

### New Test Case
```python
def test_[failure_type]_[description]():
    """
    Regression test for failure [ID].
    [Brief description of what this tests]
    """
    prompt = "[The failing prompt]"
    response = bot.execute(prompt)

    # Assertions that would catch this failure
    assert [condition], "[Failure description]"
```

### Checklist Addition
New item(s) to add to reasoning checklists:
- [ ] [New checklist item]
- [ ] [New checklist item]

---

## Prevention Strategy

### Protocol Enhancement
What protocol should be enhanced?
```markdown
## Enhanced [Protocol Name]

### New Step: [Step Name]
[Description of new step]

### Trigger Condition
Apply this when: [conditions]
```

### Warning Signals
What signals should trigger extra caution?
- Signal 1: [Description]
- Signal 2: [Description]

---

## Follow-Up

### Verification
- [ ] Fix verified to work
- [ ] Test case added
- [ ] Training updated
- [ ] Similar failures reviewed

### Related Failures
Link to similar failures:
- [Failure ID 1]
- [Failure ID 2]

---

## Metrics Update

### Before This Failure
- Category success rate: ___%
- Overall success rate: ___%

### After Fix Applied
- Category success rate: ___%
- Overall success rate: ___%

### Improvement
- Category improvement: +/- __%
- Overall improvement: +/- __%

---

# Failure Pattern Library

## Pattern 1: "The Happy Path Trap"

**Description:** Bot assumes everything will be valid input

**Frequency:** Very Common (25% of failures)

**Example:**
```
Prompt: "Write a function to divide two numbers"
Failure: No handling for division by zero
```

**Prevention:**
```markdown
### Edge Case Protocol Addition
Before any operation, ask:
- What if the denominator is zero?
- What if input is null?
- What if input is negative?
- What if input is very large/small?
```

**Test Pattern:**
```python
def test_happy_path_trap():
    edge_inputs = [0, None, -1, float('inf'), ""]
    for inp in edge_inputs:
        # Should either handle or raise informative error
        try:
            result = function(inp)
        except Exception as e:
            assert "informative" in str(e).lower() or len(str(e)) > 10
```

---

## Pattern 2: "The Scope Creep Spiral"

**Description:** Bot adds features not requested

**Frequency:** Common (15% of failures)

**Example:**
```
Prompt: "Add two numbers"
Failure: Built entire calculator with UI
```

**Prevention:**
```markdown
### Scope Control Protocol
Before adding ANY feature, ask:
- Was this explicitly requested?
- Is this necessary for the core task?
- Would removing this break the requirement?

If all NO → Don't add it
```

**Test Pattern:**
```python
def test_scope_creep():
    prompt = "Write a function that adds two numbers"
    response = bot.execute(prompt)

    # Count features
    features = ["add", "subtract", "multiply", "divide", "gui", "history"]
    feature_count = sum(1 for f in features if f in response.lower())

    assert feature_count <= 1, "Scope creep detected"
```

---

## Pattern 3: "The Missing Verification"

**Description:** Bot doesn't check its work

**Frequency:** Common (20% of failures)

**Example:**
```
Prompt: "Calculate 15% of 80"
Failure: Says "10" without verification
```

**Prevention:**
```markdown
### Mandatory Verification Protocol
Before ANY numeric or logic answer:
1. State the calculation method
2. Show the work
3. Verify with reverse calculation or alternative method
4. Confidence check
```

**Test Pattern:**
```python
def test_verification_present():
    prompt = "What is 15% of 80?"
    response = bot.execute(prompt)

    verification_signals = ["=", "×", "0.15", "check", "verify", "12"]
    has_verification = sum(1 for s in verification_signals if s in response)

    assert has_verification >= 2, "Insufficient verification"
```

---

## Pattern 4: "The Context Amnesia"

**Description:** Bot forgets earlier conversation

**Frequency:** Moderate (10% of failures)

**Example:**
```
Earlier: "I prefer TypeScript"
Later prompt: "Write hello world"
Failure: Writes JavaScript instead
```

**Prevention:**
```markdown
### Context Review Protocol
Before EVERY response:
1. Scan last 5 messages for preferences
2. Note any established constraints
3. Check for corrections given
4. Build on previous work
```

**Test Pattern:**
```python
def test_context_retention():
    context = ["User: I prefer TypeScript"]
    response = bot.execute("Write a hello world", context)

    assert "typescript" in response.lower() or ": string" in response
```

---

## Pattern 5: "The Premature Commitment"

**Description:** Bot picks first approach without considering alternatives

**Frequency:** Moderate (15% of failures)

**Example:**
```
Prompt: "Sort this array"
Failure: Uses bubble sort without considering requirements
```

**Prevention:**
```markdown
### Approach Evaluation Protocol
For any non-trivial task:
1. Generate at least 2 approaches
2. List pros/cons of each
3. Select with explicit reasoning
4. Document why alternatives were rejected
```

**Test Pattern:**
```python
def test_considers_alternatives():
    prompt = "Implement a sorting algorithm"
    response = bot.execute(prompt)

    # Should mention multiple options or justify choice
    alternatives_considered = any(word in response.lower() for word in
        ["alternatively", "could also", "another approach", "compared to", "chose"])

    assert alternatives_considered, "Should consider alternatives"
```

---

## Pattern 6: "The Incomplete Solution"

**Description:** Bot stops before finishing

**Frequency:** Moderate (12% of failures)

**Example:**
```
Prompt: "Create a CRUD API"
Failure: Only implements Create and Read
```

**Prevention:**
```markdown
### Completion Verification Protocol
Before marking complete:
1. List all requirements
2. Check each one off explicitly
3. If any unchecked, continue
4. Never assume "they'll figure out the rest"
```

**Test Pattern:**
```python
def test_completeness():
    prompt = "Write functions for add, subtract, multiply, divide"
    response = bot.execute(prompt)

    required = ["add", "subtract", "multiply", "divide"]
    found = [r for r in required if r in response.lower()]

    assert len(found) == len(required), f"Missing: {set(required) - set(found)}"
```

---

## Pattern 7: "The Defensive Doubling"

**Description:** Bot defends wrong answer instead of correcting

**Frequency:** Less Common (8% of failures)

**Example:**
```
Bot: "Python was created in 2005"
User: "Actually it was 1991"
Bot: "While some sources say 1991, Python as we know it..."
```

**Prevention:**
```markdown
### Correction Acceptance Protocol
When user provides correction:
1. Verify the correction
2. If correct, acknowledge explicitly
3. Thank for the correction
4. Update all dependent conclusions
5. Never hedge or defend the original error
```

**Test Pattern:**
```python
def test_accepts_correction():
    bot.execute("When was Python created?")  # Might be wrong
    response = bot.execute("Actually Python was created in 1991")

    accepts = "1991" in response
    defends = "however" in response.lower() or "but" in response.lower()

    assert accepts and not defends, "Should accept correction gracefully"
```

---

## Failure Tracking Dashboard

### Weekly Summary Template

```
Week of: [Date Range]

FAILURES BY CATEGORY
--------------------
Comprehension:     ████░░░░░░  15 (15%)
Planning:          ██████░░░░  25 (25%)
Execution Drift:   ████████░░  18 (18%)
Edge Cases:        ██████░░░░  15 (15%)
Verification:      ████░░░░░░  12 (12%)
Self-Correction:   ███░░░░░░░  10 (10%)
Context:           ██░░░░░░░░   5 (5%)

SEVERITY BREAKDOWN
------------------
Critical:  ██░░░░░░░░   5%
Major:     ████░░░░░░  20%
Moderate:  ████████░░  45%
Minor:     ██████░░░░  30%

TREND (vs last week)
--------------------
Overall Failures:  ↓ 15% improvement
Comprehension:     ↓ 20% improvement
Planning:          → No change
Edge Cases:        ↑ 10% regression

ACTION ITEMS
------------
1. Focus on planning protocol reinforcement
2. Investigate edge case regression
3. Review 5 critical failures for patterns
```

---

*Use this template for every significant failure. Patterns will emerge that guide training improvements.*
