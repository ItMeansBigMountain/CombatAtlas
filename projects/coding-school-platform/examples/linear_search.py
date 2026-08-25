import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from coding_school.curriculum import curriculum_catalog

linear = next(item for item in curriculum_catalog() if item.id == "student-linear-search")
namespace = {}
exec(linear.starter_code, namespace)
assert namespace["linear_search"]([55, 9, 10, 1, 5, 3, 8, 7], 5) == 4
assert namespace["linear_search"]([55, 9, 10], 100) == -1
print("Linear Search Treasure Hunt examples passed")
