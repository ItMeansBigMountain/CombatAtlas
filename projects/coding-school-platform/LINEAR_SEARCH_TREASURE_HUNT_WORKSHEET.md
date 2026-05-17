# Linear Search Treasure Hunt Worksheet

- **Project:** Coding School Platform
- **Created:** 2026-05-03
- **Source material:** `C:\Users\faree\Desktop\algos\leetCode\search.java` and `C:\Users\faree\Desktop\algos\BASIC 13 DESCRIPTIONS`
- **Copied source files:** `curriculum/source-algos/search.java`, `curriculum/source-algos/BASIC_13_DESCRIPTIONS.txt`
- **Target students:** beginner/intermediate kids or teens learning loops, arrays/lists, and problem-solving
- **Estimated time:** 45-60 minutes

## Teacher goal

Students should understand that **linear search** means checking items one by one until the target is found or the list ends.

This lesson is based on the Java source pattern:

```java
public static int search(int[] nums, int target) {
    int index = -1;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == target) {
            return i;
        }
    }
    return index;
}
```

## Student-friendly story

You are a treasure hunter searching a row of treasure chests.

Each chest has a number on it:

```text
[55, 9, 10, 1, 5, 3, 8, 7]
```

Your mission: find the chest with treasure number `5`.

You cannot magically jump to the answer. You must check one chest at a time from left to right.

## Key vocabulary

| Word | Meaning |
|---|---|
| Array / list | A row of values stored together |
| Index | The position number of an item in the list |
| Target | The value we are trying to find |
| Loop | Code that repeats steps |
| Condition | A true/false check, usually with `if` |
| Return | Send the answer back |
| `-1` | Common code meaning “not found” |

## Warm-up: index practice

Given this list:

```text
index:  0   1   2   3   4   5   6   7
value: 55   9  10   1   5   3   8   7
```

Answer:

1. What value is at index `0`?
2. What value is at index `4`?
3. What index contains the value `10`?
4. What index contains the value `7`?
5. If the target is `5`, what should the search return?

## Algorithm idea

Linear search follows this plan:

```text
Start at the first item.
Check: is this item the target?
If yes, return the index.
If no, move to the next item.
If the list ends, return -1.
```

## Python version

```python
def linear_search(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1

numbers = [55, 9, 10, 1, 5, 3, 8, 7]
print(linear_search(numbers, 5))
```

Expected output:

```text
4
```

## JavaScript version

```javascript
function linearSearch(nums, target) {
  for (let i = 0; i < nums.length; i++) {
    if (nums[i] === target) {
      return i;
    }
  }
  return -1;
}

const numbers = [55, 9, 10, 1, 5, 3, 8, 7];
console.log(linearSearch(numbers, 5));
```

Expected output:

```text
4
```

## Trace table activity

Fill this out while searching for target `5`.

| Step | Index `i` | Value `nums[i]` | Is it target `5`? | Action |
|---:|---:|---:|---|---|
| 1 | 0 | 55 | no | keep searching |
| 2 | 1 | 9 | no | keep searching |
| 3 | 2 | 10 | no | keep searching |
| 4 | 3 | 1 | no | keep searching |
| 5 | 4 | 5 | yes | return 4 |

## Coding challenge 1: find the key

Change the target to `8`.

Questions:

1. What index should be returned?
2. How many checks does the computer make?
3. Why does it not check the values after `8`?

## Coding challenge 2: not found

Search for `100`.

Questions:

1. What should the function return?
2. Why does the function return `-1`?
3. How many values were checked?

## Coding challenge 3: make it say more

Modify the function so it prints what it is checking.

Python hint:

```python
print("Checking index", i, "value", nums[i])
```

Expected style:

```text
Checking index 0 value 55
Checking index 1 value 9
Checking index 2 value 10
Checking index 3 value 1
Checking index 4 value 5
Found at index 4
```

## Extension: treasure names

Now search a list of treasure names:

```python
treasures = ["coin", "map", "potion", "key", "gem"]
```

Find:

1. `"key"`
2. `"coin"`
3. `"dragon"`

## Discussion questions

1. Is linear search fast or slow for a huge list?
2. What happens if the target is the first item?
3. What happens if the target is the last item?
4. What happens if the target is not there?
5. Why do programmers often return `-1` for not found?

## Teacher notes

### Common student mistake

Students may confuse value and index.

Example:

- Value `5` is not the answer.
- The answer is index `4` because `5` lives at position `4`.

### Coaching phrase

"The value is the treasure. The index is the address."

### Link to Basic 13 source

This lesson builds on Basic 13 ideas:

- print all values in an array
- print maximum value in an array
- print items greater than 10

Those all require walking through a list one item at a time, just like linear search.

## Exit ticket

Before leaving, students answer:

1. In one sentence, what does linear search do?
2. What does the function return when it finds the target?
3. What does the function return when it does not find the target?
4. Write one real-life example of linear search.

## Validation checklist

- [ ] Student can explain target vs index.
- [ ] Student can trace the list by hand.
- [ ] Student can run or read the Python/JavaScript version.
- [ ] Student can explain why `-1` means not found.

## Mission card

```text
Mission: Find the hidden treasure number.
Tool: Linear search.
Rule: Check each chest from left to right.
Win condition: Return the index where the treasure is found.
Failure condition: Return -1 if the treasure is missing.
```

## Read / Predict / Run / Fix / Challenge

### 1. Read

Read this code without running it:

```python
def linear_search(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1
```

Circle or underline:

- the loop
- the condition
- the return when found
- the return when not found

### 2. Predict

For this list:

```python
numbers = [55, 9, 10, 1, 5, 3, 8, 7]
```

Predict the output:

```python
print(linear_search(numbers, 3))
print(linear_search(numbers, 99))
```

### 3. Run

Run the code and compare your prediction to the actual output.

If your prediction was wrong, write what confused you:

```text
I thought ______, but the computer did ______.
```

### 4. Fix

This version has a bug. Fix it:

```python
def broken_search(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return nums[i]
    return -1
```

Hint: should the function return the value or the index?

### 5. Challenge

Write a new function that returns how many checks it made before finding the target.

Example:

```text
Searching for 5 in [55, 9, 10, 1, 5, 3, 8, 7]
Checks made: 5
```

## AI reflection section

Ask an AI assistant:

```text
Explain linear search to a 10-year-old using a treasure hunt analogy.
```

Then answer:

1. What did the AI explain well?
2. What did it leave out?
3. Did it explain index vs value clearly?
4. What would you change to make the explanation better?

Teacher note: this reinforces that AI can explain, but students still need to trace and verify the code themselves.
