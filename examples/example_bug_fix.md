# Example: Bug Fix Using the Reasoning Framework

This example demonstrates how to apply the 5-Phase Reasoning Model to diagnose and fix a bug in a Python function.

## The Problem

A user reports that their `calculate_average` function returns incorrect results for certain inputs:

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

The user says: "It crashes when I pass an empty list!"

---

## Phase 1: Comprehension

### What is being asked?
- Fix a bug in the `calculate_average` function
- The function crashes with empty lists

### Requirements Analysis
- [ ] Function should handle empty lists gracefully
- [ ] Function should return correct average for valid inputs
- [ ] Function should have clear error handling

### Input/Output Specifications
- **Input**: A list of numbers (integers or floats)
- **Expected Output**: The arithmetic mean of the numbers
- **Edge Cases**: Empty list, single element, negative numbers, mixed types

### Problem Restatement
The function divides by `len(numbers)` which causes a `ZeroDivisionError` when the list is empty. We need to handle this edge case.

---

## Phase 2: Strategy

### Possible Approaches

#### Approach A: Return None for empty lists
- **Pros**: Simple, clear indication of no data
- **Cons**: Caller must check for None

#### Approach B: Raise a descriptive exception
- **Pros**: Explicit error, follows Python conventions
- **Cons**: Caller must handle exception

#### Approach C: Return 0 for empty lists
- **Pros**: Always returns a number
- **Cons**: Mathematically incorrect, hides the error

### Selected Approach
**Approach B**: Raise a `ValueError` with a descriptive message. This follows Python conventions and makes the error explicit.

### Execution Plan
1. Add check for empty list at function start
2. Raise `ValueError` if list is empty
3. Keep existing logic for valid inputs
4. Add docstring explaining behavior

---

## Phase 3: Execution

### Step 1: Add empty check

```python
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
```

### Step 2: Preserve working logic

```python
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

### Step 3: Add docstring

```python
def calculate_average(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numeric values (int or float)

    Returns:
        The arithmetic mean of the input numbers

    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

---

## Phase 4: Review

### Requirements Verification
- [x] Function handles empty lists gracefully (raises clear error)
- [x] Function returns correct average for valid inputs
- [x] Function has clear error handling with descriptive message

### Edge Case Coverage
- [x] Empty input → Raises `ValueError`
- [x] Single element → Returns that element (tested mentally: `[5]` → `5.0`)
- [x] Negative numbers → Works correctly (tested mentally: `[-1, 1]` → `0.0`)
- [x] Zero values → Works correctly (tested mentally: `[0, 0]` → `0.0`)

### Code Quality Check
- [x] Code runs without errors
- [x] Correct output for normal inputs
- [x] Edge cases handled
- [x] Readable and well-formatted
- [x] Includes documentation
- [x] No security vulnerabilities

### Self-Critique
- **Accuracy**: Solution correctly addresses the ZeroDivisionError ✓
- **Completeness**: All requirements addressed ✓
- **Quality**: Follows Python conventions ✓

---

## Phase 5: Refinement

### Potential Improvement: Use built-in sum()

The loop can be simplified using Python's built-in `sum()` function:

```python
def calculate_average(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numeric values (int or float)

    Returns:
        The arithmetic mean of the input numbers

    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    return sum(numbers) / len(numbers)
```

### Final Verification

| Test Case | Input | Expected | Actual | Pass |
|-----------|-------|----------|--------|------|
| Normal | `[1, 2, 3]` | `2.0` | `2.0` | ✓ |
| Empty | `[]` | `ValueError` | `ValueError` | ✓ |
| Single | `[5]` | `5.0` | `5.0` | ✓ |
| Negative | `[-2, 2]` | `0.0` | `0.0` | ✓ |
| Floats | `[1.5, 2.5]` | `2.0` | `2.0` | ✓ |

---

## Summary

### Before (Problematic Code)
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Crashes on empty list!
```

### After (Fixed Code)
```python
def calculate_average(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numeric values (int or float)

    Returns:
        The arithmetic mean of the input numbers

    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    return sum(numbers) / len(numbers)
```

### Key Improvements
1. **Error Handling**: Empty list now raises descriptive `ValueError`
2. **Documentation**: Added docstring explaining usage and exceptions
3. **Simplification**: Used built-in `sum()` for cleaner code
4. **Robustness**: All edge cases now handled appropriately
