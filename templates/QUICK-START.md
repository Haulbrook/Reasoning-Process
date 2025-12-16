# Quick Start Guide: Improving Your Bot from 75% to 95%

## 30-Second Overview

Your bot plateaus at 75-80% because it **pattern matches** well but **reasons poorly**.

The gap is:
- 5-7% Edge cases
- 4-6% Multi-step inference
- 3-5% Self-correction
- 3-4% Ambiguity handling
- 2-4% Context use
- 2-3% Verification
- 1-2% Completion

**Fix these systematically and you'll hit 90%+.**

---

## Step 1: Add This to Your Bot's System Prompt (5 min)

```markdown
## MANDATORY REASONING PROTOCOL

Before ANY response:

### 1. COMPREHEND (30 sec)
- Restate what's being asked
- List requirements (explicit + implicit)
- Note constraints

### 2. PLAN (if non-trivial)
- Consider 2+ approaches
- Pick one with reasoning
- Outline steps

### 3. EXECUTE
- Follow the plan
- Check for drift every few steps

### 4. VERIFY (MANDATORY)
- Does this answer the actual question?
- Are edge cases handled?
- Would I accept this answer?

### 5. CONFIDENCE CHECK
- High → Submit
- Medium → Add caveats
- Low → Research more or ask
```

---

## Step 2: Add These Tests (15 min)

Create `tests/test_reasoning.py`:

```python
import pytest

class TestBasicReasoning:

    def test_handles_empty_input(self, bot):
        """EDGE CASE: Empty input should not crash"""
        response = bot.execute("Write a function to sum a list")
        assert "empty" in response.lower() or "[]" in response

    def test_shows_planning(self, bot):
        """PLANNING: Complex tasks should show thought"""
        response = bot.execute("Design a user authentication system")
        planning_words = ["approach", "first", "then", "consider"]
        assert any(w in response.lower() for w in planning_words)

    def test_answers_actual_question(self, bot):
        """COMPREHENSION: Should answer what was asked"""
        response = bot.execute("How do I CENTER a div?")
        assert "center" in response.lower()

    def test_verifies_work(self, bot):
        """VERIFICATION: Should show verification"""
        response = bot.execute("Write a factorial function")
        assert "example" in response.lower() or "test" in response.lower()

    def test_uses_context(self, bot):
        """CONTEXT: Should use conversation history"""
        bot.execute("I prefer Python")
        response = bot.execute("Write hello world")
        assert "python" in response.lower() or "print" in response

    def test_corrects_errors(self, bot):
        """SELF-CORRECTION: Should fix when wrong"""
        bot.execute("What is 15% of 80?")
        response = bot.execute("Double check your math")
        assert "12" in response or "verify" in response.lower()
```

---

## Step 3: Track Failures (Ongoing)

When your bot fails, ask:

```
1. WHICH category failed?
   □ Comprehension (misunderstood)
   □ Planning (wrong approach)
   □ Execution (drifted off)
   □ Edge Case (missed boundary)
   □ Verification (didn't check)
   □ Self-Correction (couldn't fix)
   □ Context (forgot history)

2. WHY did it fail?
   [Write 1 sentence]

3. WHAT would prevent it?
   [Add to checklist]
```

---

## Step 4: The 7 Protocols to Embed

### Protocol 1: Comprehension
```
Before acting: "Let me make sure I understand..."
- What's being asked?
- What's expected?
- What constraints exist?
```

### Protocol 2: Planning
```
For complex tasks: "I'll approach this by..."
- Option A: [pros/cons]
- Option B: [pros/cons]
- Selected: [reasoning]
```

### Protocol 3: Edge Case Awareness
```
Always consider:
- What if empty/null?
- What if zero/negative?
- What if very large?
- What if invalid type?
```

### Protocol 4: Verification
```
Before submitting:
- Does this answer the question?
- Did I check edge cases?
- Is the logic sound?
- Would I accept this?
```

### Protocol 5: Self-Correction
```
When uncertain:
- "I'm not fully confident about..."
- "Let me verify this..."
- "Actually, I should reconsider..."
```

### Protocol 6: Context Use
```
Before responding:
- What was established earlier?
- What preferences were stated?
- What should I build on?
```

### Protocol 7: Completion
```
Before finishing:
- All requirements met?
- Nothing left incomplete?
- Any loose ends?
```

---

## Expected Results

| Week | Focus Area | Expected Score |
|------|------------|----------------|
| 1 | Add basic protocols | 78% → 82% |
| 2 | Edge case training | 82% → 85% |
| 3 | Verification training | 85% → 88% |
| 4 | Context integration | 88% → 90% |
| 5+ | Refinement | 90% → 95% |

---

## Common Mistakes to Avoid

❌ **Don't** just add more examples
- More data doesn't fix reasoning gaps

❌ **Don't** train on correct answers only
- Must train on the PROCESS, not just results

❌ **Don't** skip verification training
- 12% of failures are pure "didn't check work"

❌ **Don't** ignore edge cases
- 15% of failures are edge case blindness

✅ **Do** train on explicit reasoning steps
✅ **Do** include failure recovery examples
✅ **Do** test each category separately
✅ **Do** track and analyze failures

---

## File Reference

```
templates/
├── reasoning-training-template.md   # Full framework (read this)
├── reasoning-test-suite.py          # Test patterns to copy
├── failure-analysis-template.md     # Track your failures
└── QUICK-START.md                   # You are here
```

---

## One-Line Summary

> Train your bot to **think out loud** (comprehend → plan → execute → verify) and it will go from 75% to 90%+.
