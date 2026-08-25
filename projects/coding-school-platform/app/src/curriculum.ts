export type Lesson = {
  id: string;
  title: string;
  module: string;
  description: string;
  starterCode: string;
  rubric: string[];
};

const basicTitles = [
  'Print 1-255', 'Print odd numbers 1-255', 'Sum 1-255', 'Print list values',
  'Find maximum', 'Find average', 'Collect odd numbers', 'Square values',
  'Count above threshold', 'Convert matches to zero', 'Min, max, average',
  'Shift list values', 'Replace negatives',
];

export const lessons: Lesson[] = [
  ...basicTitles.map((title, index) => ({
    id: `student-basic-${String(index + 1).padStart(2, '0')}`,
    title,
    module: 'Basic 13',
    description: 'Read, predict, run, fix, challenge, then reflect.',
    starterCode: `# ${title}\nnums = [3, -1, 8, 4]\n# Write your solution here\n`,
    rubric: ['Read the prompt', 'Predict the output', 'Test the code', 'Explain one choice'],
  })),
  {
    id: 'student-linear-search',
    title: 'Linear Search Treasure Hunt',
    module: 'Algorithm Academy',
    description: 'Trace a target, return its index, and handle a missing value.',
    starterCode: 'def linear_search(nums, target):\n    for index, value in enumerate(nums):\n        # Your condition here\n        pass\n    return -1\n',
    rubric: ['Trace target', 'Return index', 'Handle not found', 'Explain index vs value'],
  },
];

export const safeHints = [
  'Trace one loop iteration at a time and write down index and value.',
  'Try the smallest useful input before adding more cases.',
  'Explain what you expect first; then compare it with what happened.',
];
