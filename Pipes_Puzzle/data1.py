"""
Note:
    In each level 5x5 Pipes:
        set index (x, y) start with bottom-left = (0, 0)
        increase x when through to top
        increase y when through to right
        each cell is a dict with two keys: type, heading.

    key ["type"]:
        value = 1 ==> Dead-end pipes
        value = 2 ==> Straight line pipes
        value = 3 ==> Elbow pipes
        value = 4 ==> T-joint pipes

    key ["heading"]:
        value = 0 ==> Eastern ">" 
        value = 90 ==> Southern "v"
        value = 180 ==> Western "<"
        value = 270 ==> Northern "^"

TEST: 8 Levels
- Levels 1 -> 5: Solvable (Scrambled initial states)
- Level 8: Unsolvable (Isolated Corner)
- Level 9: Unsolvable (All Straight Pipes)
- Level 10: Unsolvable (Starved Center)
"""

HEADING = [0, 90, 180, 270]

TESTCASE = {
    # ========== SOLVABLE LEVELS ==========
    "level 1": [
        [{"type": 3, "heading": 180}, {"type": 4, "heading": 270}, {"type": 3, "heading": 90}, {"type": 1, "heading": 0}, {"type": 1, "heading": 90}],
        [{"type": 1, "heading": 0}, {"type": 2, "heading": 0}, {"type": 4, "heading": 90}, {"type": 3, "heading": 180}, {"type": 2, "heading": 0}],
        [{"type": 1, "heading": 90}, {"type": 1, "heading": 180}, {"type": 4, "heading": 90}, {"type": 4, "heading": 270}, {"type": 4, "heading": 90}],
        [{"type": 3, "heading": 180}, {"type": 4, "heading": 270}, {"type": 4, "heading": 90}, {"type": 2, "heading": 90}, {"type": 2, "heading": 90}],
        [{"type": 1, "heading": 270}, {"type": 3, "heading": 90}, {"type": 1, "heading": 0}, {"type": 1, "heading": 90}, {"type": 1, "heading": 90}]
    ],
    "level 2": [
        [{"type": 3, "heading": 270}, {"type": 1, "heading": 180}, {"type": 1, "heading": 90}, {"type": 1, "heading": 90}, {"type": 3, "heading": 0}],
        [{"type": 4, "heading": 270}, {"type": 1, "heading": 0}, {"type": 2, "heading": 0}, {"type": 3, "heading": 270}, {"type": 3, "heading": 0}],
        [{"type": 3, "heading": 270}, {"type": 4, "heading": 270}, {"type": 4, "heading": 90}, {"type": 2, "heading": 90}, {"type": 1, "heading": 180}],
        [{"type": 3, "heading": 270}, {"type": 3, "heading": 180}, {"type": 4, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 0}],
        [{"type": 1, "heading": 180}, {"type": 1, "heading": 90}, {"type": 4, "heading": 180}, {"type": 2, "heading": 90}, {"type": 1, "heading": 0}]
    ],
    "level 3": [
        [{"type": 1, "heading": 90}, {"type": 1, "heading": 270}, {"type": 1, "heading": 180}, {"type": 1, "heading": 270}, {"type": 1, "heading": 180}],
        [{"type": 4, "heading": 90}, {"type": 3, "heading": 90}, {"type": 4, "heading": 270}, {"type": 4, "heading": 180}, {"type": 4, "heading": 0}],
        [{"type": 4, "heading": 0}, {"type": 4, "heading": 180}, {"type": 4, "heading": 0}, {"type": 3, "heading": 180}, {"type": 1, "heading": 0}],
        [{"type": 2, "heading": 90}, {"type": 2, "heading": 90}, {"type": 1, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 270}],
        [{"type": 1, "heading": 180}, {"type": 1, "heading": 90}, {"type": 3, "heading": 0}, {"type": 3, "heading": 180}, {"type": 1, "heading": 180}]
    ],
    "level 4": [
        [{"type": 1, "heading": 180}, {"type": 1, "heading": 180}, {"type": 3, "heading": 270}, {"type": 1, "heading": 180}, {"type": 1, "heading": 90}],
        [{"type": 4, "heading": 0}, {"type": 4, "heading": 180}, {"type": 4, "heading": 270}, {"type": 4, "heading": 0}, {"type": 2, "heading": 180}],
        [{"type": 2, "heading": 90}, {"type": 2, "heading": 90}, {"type": 3, "heading": 180}, {"type": 4, "heading": 90}, {"type": 4, "heading": 180}],
        [{"type": 1, "heading": 90}, {"type": 2, "heading": 180}, {"type": 4, "heading": 90}, {"type": 3, "heading": 90}, {"type": 2, "heading": 90}],
        [{"type": 1, "heading": 270}, {"type": 3, "heading": 180}, {"type": 1, "heading": 90}, {"type": 1, "heading": 0}, {"type": 1, "heading": 0}]
    ],
    "level 5": [
        [{"type": 1, "heading": 270}, {"type": 1, "heading": 180}, {"type": 1, "heading": 90}, {"type": 4, "heading": 0}, {"type": 1, "heading": 270}],
        [{"type": 3, "heading": 0}, {"type": 4, "heading": 90}, {"type": 3, "heading": 180}, {"type": 4, "heading": 90}, {"type": 1, "heading": 270}],
        [{"type": 3, "heading": 180}, {"type": 3, "heading": 90}, {"type": 3, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 180}],
        [{"type": 4, "heading": 270}, {"type": 2, "heading": 90}, {"type": 4, "heading": 270}, {"type": 4, "heading": 90}, {"type": 2, "heading": 180}],
        [{"type": 3, "heading": 0}, {"type": 1, "heading": 0}, {"type": 1, "heading": 180}, {"type": 1, "heading": 270}, {"type": 1, "heading": 0}]
    ],

    # ========== UNSOLVABLE LEVELS (TRAPS) ==========
    "level 6": [
        [{"type": 3, "heading": 0}, {"type": 1, "heading": 90}, {"type": 4, "heading": 90}, {"type": 4, "heading": 90}, {"type": 3, "heading": 270}],
        [{"type": 1, "heading": 0}, {"type": 4, "heading": 0}, {"type": 3, "heading": 180}, {"type": 3, "heading": 270}, {"type": 4, "heading": 0}],
        [{"type": 4, "heading": 180}, {"type": 4, "heading": 90}, {"type": 4, "heading": 0}, {"type": 4, "heading": 180}, {"type": 4, "heading": 270}],
        [{"type": 4, "heading": 0}, {"type": 3, "heading": 90}, {"type": 3, "heading": 0}, {"type": 4, "heading": 90}, {"type": 4, "heading": 270}],
        [{"type": 3, "heading": 90}, {"type": 4, "heading": 180}, {"type": 4, "heading": 270}, {"type": 4, "heading": 0}, {"type": 3, "heading": 180}]
    ],
    "level 7": [
        [{"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}],
        [{"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}],
        [{"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}],
        [{"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}],
        [{"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}, {"type": 2, "heading": 90}, {"type": 2, "heading": 0}]
    ],
    "level 8": [
        [{"type": 3, "heading": 0}, {"type": 4, "heading": 90}, {"type": 4, "heading": 180}, {"type": 4, "heading": 270}, {"type": 3, "heading": 270}],
        [{"type": 4, "heading": 0}, {"type": 3, "heading": 90}, {"type": 1, "heading": 180}, {"type": 3, "heading": 270}, {"type": 4, "heading": 180}],
        [{"type": 4, "heading": 90}, {"type": 1, "heading": 0}, {"type": 4, "heading": 0}, {"type": 1, "heading": 180}, {"type": 4, "heading": 270}],
        [{"type": 4, "heading": 180}, {"type": 3, "heading": 0}, {"type": 1, "heading": 0}, {"type": 3, "heading": 180}, {"type": 4, "heading": 0}],
        [{"type": 3, "heading": 90}, {"type": 4, "heading": 270}, {"type": 4, "heading": 0}, {"type": 4, "heading": 90}, {"type": 3, "heading": 180}]
    ]
}