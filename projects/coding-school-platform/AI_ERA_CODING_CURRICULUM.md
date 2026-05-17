# AI-Era Coding Curriculum for Kids and Teens

- **Date:** 2026-05-03
- **Business context:** Affan teaches kids/teens how to code.
- **Source inspiration:** `C:\Users\faree\Desktop\algos`
- **Teaching philosophy:** Kids should learn to think, read, and reason in code — not just memorize syntax. In the LLM era, they must understand what code can do, how to describe systems, how to debug, and how to judge AI-generated code.

## Core outcome

Students should be able to say:

> “I can read code, explain what it does, change it safely, debug it, and use AI as a helper without being fooled by it.”

## Level structure

| Level | Age band | Focus | Output |
| --- | --- | --- | --- |
| Level 0 | 6-8 | Sequencing, patterns, commands, cause/effect | Scratch-style mini games and movement puzzles |
| Level 1 | 8-10 | Variables, conditions, loops, lists | Simple Python/Scratch games and story choices |
| Level 2 | 10-12 | Functions, data structures, search/sort intuition | Algorithm visualizers and small utilities |
| Level 3 | 12-14 | Problem solving, debugging, APIs, files | Mini apps, bots, dashboards, data projects |
| Level 4 | 14-17 | Architecture, AI-assisted coding, web/cloud basics | Portfolio projects with LLM-assisted workflows |

## Curriculum spine

### Module 1: Think Like a Computer

Goal: understand exact instructions.

Lessons:

1. Commands and sequence
2. Inputs and outputs
3. If/then decisions
4. Loops as repeated behavior
5. Bugs as broken instructions, not personal failure

Activities:

- Human robot game
- Scratch maze
- “Give instructions to make a sandwich” debugging exercise

### Module 2: Variables and State

Goal: understand memory and changing values.

Lessons:

1. Variables as named boxes
2. Scores, health, inventory
3. Updating values
4. Reading state to decide what happens next

Projects:

- Score counter
- Clicker game
- Pet simulator

### Module 3: Conditions and Game Logic

Goal: understand decisions in code.

Lessons:

1. `if`, `elif`, `else`
2. Boolean thinking
3. Game win/loss rules
4. Nested choices

Projects:

- Choose-your-own-adventure story
- Quiz game
- Door/key puzzle

### Module 4: Loops and Patterns

Goal: understand repetition and automation.

Lessons:

1. `for` loops
2. `while` loops
3. Repeating over lists
4. Infinite loop safety

Projects:

- Multiplication trainer
- Sprite animation loop
- Pattern drawer

### Module 5: Lists and Collections

Goal: understand groups of things.

Lessons:

1. Lists as ordered collections
2. Adding/removing items
3. Looping through lists
4. Finding the biggest/smallest item

Projects:

- Inventory system
- Favorite games/music analyzer
- Random name picker

### Module 6: Algorithms as Brain Teasers

Source material from `algos`:

- `linear_search.py`
- `binary_search.py`
- `recursiveBinarySearch.py`
- `bubbleSort.py`
- `insertionSort.py`
- `mergeSort.py`
- `LinkedList.py`
- `factorials.py`
- `longestCommonPrefix.py`

Goal: students learn how to read logic and compare strategies.

Lessons:

1. Linear search: “check every locker”
2. Binary search: “guess the number intelligently”
3. Bubble sort: “swap neighbors”
4. Insertion sort: “sort cards in your hand”
5. Merge sort: “divide, solve, combine”
6. Recursion: “a function asking a smaller version of itself”
7. Linked lists: “treasure map nodes”

Teaching style:

- Start unplugged with cards/number lines.
- Then read code line by line.
- Then predict output.
- Then modify one thing.
- Then ask AI to explain it and critique the AI answer.

### Module 7: Debugging and Reading Code

Goal: become comfortable with unfamiliar code.

Lessons:

1. Read filenames and comments first
2. Find inputs and outputs
3. Trace variables
4. Add print statements
5. Make one small change at a time
6. Compare expected vs actual

Exercises:

- Broken sorting script
- Off-by-one bug
- Wrong variable name
- Infinite loop rescue

### Module 8: Building Real Things

Goal: show what code can do.

Project tracks:

1. Games
   - Dodge game
   - Quiz game
   - Platformer logic
2. Web apps
   - Personal page
   - Leaderboard
   - Class project gallery
3. Data apps
   - Favorite music survey
   - Sports stats chart
   - Stock/news sentiment demo with sample data
4. Bots/automation
   - Reminder bot
   - Homework helper script
   - File organizer

### Module 9: Coding with AI Without Becoming Lazy

Goal: teach AI-assisted development responsibly.

Rules for students:

1. Ask AI for hints before full answers.
2. Always explain AI code in your own words.
3. Run the code before trusting it.
4. Change one thing and predict what happens.
5. Never paste secrets or personal info.
6. Use AI to learn faster, not to skip thinking.

Exercises:

- Ask AI to explain binary search, then spot what it missed.
- Ask AI for a bug fix, then test if it worked.
- Ask AI for three project ideas, then choose one and break it into steps.

## First 12-week beginner track

| Week | Topic | Student output |
| ---: | --- | --- |
| 1 | Commands, sequence, Scratch/Python intro | Movement maze |
| 2 | Variables and score | Clicker/score game |
| 3 | Conditions | Quiz or door/key game |
| 4 | Loops | Pattern or multiplication trainer |
| 5 | Lists | Inventory/random picker |
| 6 | Functions | Reusable game actions |
| 7 | Linear search | Find item game |
| 8 | Binary search | Guessing strategy visualizer |
| 9 | Sorting with cards | Bubble/insertion sort visual demo |
| 10 | Debugging | Fix broken mini programs |
| 11 | AI helper workflow | Use AI to improve a project safely |
| 12 | Capstone demo day | Student presents project + explains code |

## First worksheet format

Each worksheet should include:

1. **Mission:** What are we building?
2. **Concept:** One idea only.
3. **Read the code:** Small snippet.
4. **Predict:** What happens before running it?
5. **Run:** Execute and observe.
6. **Fix/change:** One missing line or bug.
7. **Challenge:** Add one feature.
8. **AI reflection:** Ask AI a question, then verify the answer.

## First concrete worksheet candidates from `algos`

1. Linear Search Treasure Hunt
2. Binary Search Guessing Game
3. Bubble Sort Race
4. Factorial Staircase
5. Longest Common Prefix Word Detective
6. Linked List Treasure Map

## Next build task

Copy selected `algos` files into `coding-school-platform/legacy-src/algos`, then create the first worksheet: **Linear Search Treasure Hunt**.
