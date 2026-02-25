"""
Dữ liệu thay thế cho data.py (10 level).
Level 1-5: có lời giải. Level 6-8: không có lời giải (góc tách biệt, toàn ống thẳng, ...).
Định dạng ô giống data.py.
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