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
"""

HEADING = [0, 90, 180, 270]

TESTCASE = {
    "level 0": [
        [{"type": 3, "heading": 0}, {"type": 4, "heading": 270}, {"type": 3, "heading": 180}, {"type": 1, "heading": 270}, {"type": 1, "heading": 270}],
        [{"type": 1, "heading": 90}, {"type": 2, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 90}, {"type": 2, "heading": 90}],
        [{"type": 1, "heading": 270}, {"type": 1, "heading": 90}, {"type": 4, "heading": 0}, {"type": 4, "heading": 270}, {"type": 4, "heading": 180}],
        [{"type": 3, "heading": 0}, {"type": 4, "heading": 270}, {"type": 4, "heading": 180}, {"type": 2, "heading": 90}, {"type": 2, "heading": 90}],
        [{"type": 1, "heading": 0}, {"type": 3, "heading": 90}, {"type": 1, "heading": 90}, {"type": 1, "heading": 90}, {"type": 1, "heading": 180}]
    ],
    "level 1": [
        [{"type": 3, "heading": 90}, {"type": 4, "heading": 90}, {"type": 3, "heading": 0}, {"type": 1, "heading": 180}, {"type": 1, "heading": 0}],
        [{"type": 1, "heading": 90}, {"type": 2, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 90}, {"type": 2, "heading": 90}],
        [{"type": 1, "heading": 270}, {"type": 1, "heading": 90}, {"type": 4, "heading": 0}, {"type": 4, "heading": 180}, {"type": 4, "heading": 0}],
        [{"type": 3, "heading": 90}, {"type": 4, "heading": 180}, {"type": 4, "heading": 0}, {"type": 2, "heading": 0}, {"type": 2, "heading": 0}],
        [{"type": 1, "heading": 180}, {"type": 3, "heading": 0}, {"type": 1, "heading": 90}, {"type": 1, "heading": 270}, {"type": 1, "heading": 0}]
    ],
    "level 2": [
        [{"type": 1, "heading": 180}, {"type": 3, "heading": 90}, {"type": 3, "heading": 90}, {"type": 2, "heading": 0}, {"type": 1, "heading": 90}],
        [{"type": 3, "heading": 90}, {"type": 3, "heading": 270}, {"type": 4, "heading": 0}, {"type": 4, "heading": 0}, {"type": 3, "heading": 270}],
        [{"type": 4, "heading": 180}, {"type": 2, "heading": 0}, {"type": 4, "heading": 270}, {"type": 2, "heading": 90}, {"type": 2, "heading": 90}],
        [{"type": 1, "heading": 0}, {"type": 1, "heading": 0}, {"type": 4, "heading": 180}, {"type": 1, "heading": 270}, {"type": 1, "heading": 270}],
        [{"type": 1, "heading": 0}, {"type": 2, "heading": 90}, {"type": 4, "heading": 180}, {"type": 2, "heading": 90}, {"type": 1, "heading": 270}]
    ],
    "level 3": [
        [{"type": 3, "heading": 180}, {"type": 1, "heading": 90}, {"type": 1, "heading": 0}, {"type": 1, "heading": 0}, {"type": 3, "heading": 270}],
        [{"type": 4, "heading": 180}, {"type": 1, "heading": 270}, {"type": 2, "heading": 90}, {"type": 3, "heading": 180}, {"type": 3, "heading": 270}],
        [{"type": 3, "heading": 180}, {"type": 4, "heading": 180}, {"type": 4, "heading": 0}, {"type": 2, "heading": 0}, {"type": 1, "heading": 90}],
        [{"type": 3, "heading": 180}, {"type": 3, "heading": 90}, {"type": 4, "heading": 0}, {"type": 4, "heading": 270}, {"type": 3, "heading": 270}],
        [{"type": 1, "heading": 90}, {"type": 1, "heading": 0}, {"type": 4, "heading": 90}, {"type": 2, "heading": 0}, {"type": 1, "heading": 270}]
    ],
    "level 4": [
        [{"type": 1, "heading": 0}, {"type": 1, "heading": 180}, {"type": 1, "heading": 90}, {"type": 1, "heading": 180}, {"type": 1, "heading": 90}],
        [{"type": 4, "heading": 0}, {"type": 3, "heading": 0}, {"type": 4, "heading": 180}, {"type": 4, "heading": 90}, {"type": 4, "heading": 270}],
        [{"type": 4, "heading": 270}, {"type": 4, "heading": 90}, {"type": 4, "heading": 270}, {"type": 3, "heading": 90}, {"type": 1, "heading": 270}],
        [{"type": 2, "heading": 0}, {"type": 2, "heading": 0}, {"type": 1, "heading": 0}, {"type": 4, "heading": 270}, {"type": 3, "heading": 180}],
        [{"type": 1, "heading": 90}, {"type": 1, "heading": 0}, {"type": 3, "heading": 270}, {"type": 3, "heading": 90}, {"type": 1, "heading": 90}]
    ],
    "level 5": [
        [{"type": 3, "heading": 270}, {"type": 2, "heading": 90}, {"type": 1, "heading": 0}, {"type": 3, "heading": 90}, {"type": 1, "heading": 180}],
        [{"type": 3, "heading": 0}, {"type": 4, "heading": 180}, {"type": 1, "heading": 270}, {"type": 4, "heading": 90}, {"type": 1, "heading": 270}],
        [{"type": 1, "heading": 0}, {"type": 4, "heading": 90}, {"type": 4, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 270}],
        [{"type": 1, "heading": 0}, {"type": 4, "heading": 0}, {"type": 4, "heading": 0}, {"type": 1, "heading": 270}, {"type": 1, "heading": 0}],
        [{"type": 1, "heading": 0}, {"type": 3, "heading": 180}, {"type": 3, "heading": 180}, {"type": 4, "heading": 90}, {"type": 1, "heading": 90}]
    ],
    "level 6": [
        [{"type": 1, "heading": 90}, {"type": 1, "heading": 90}, {"type": 3, "heading": 180}, {"type": 1, "heading": 90}, {"type": 1, "heading": 0}],
        [{"type": 4, "heading": 270}, {"type": 4, "heading": 90}, {"type": 4, "heading": 180}, {"type": 4, "heading": 270}, {"type": 2, "heading": 90}],
        [{"type": 2, "heading": 0}, {"type": 2, "heading": 0}, {"type": 3, "heading": 90}, {"type": 4, "heading": 0}, {"type": 4, "heading": 90}],
        [{"type": 1, "heading": 0}, {"type": 2, "heading": 90}, {"type": 4, "heading": 0}, {"type": 3, "heading": 0}, {"type": 2, "heading": 0}],
        [{"type": 1, "heading": 180}, {"type": 3, "heading": 90}, {"type": 1, "heading": 0}, {"type": 1, "heading": 270}, {"type": 1, "heading": 270}]
    ],
    "level 7": [
        [{"type": 1, "heading": 180}, {"type": 1, "heading": 90}, {"type": 1, "heading": 0}, {"type": 4, "heading": 270}, {"type": 1, "heading": 180}],
        [{"type": 3, "heading": 270}, {"type": 4, "heading": 0}, {"type": 3, "heading": 90}, {"type": 4, "heading": 0}, {"type": 1, "heading": 180}],
        [{"type": 3, "heading": 90}, {"type": 3, "heading": 0}, {"type": 3, "heading": 0}, {"type": 4, "heading": 270}, {"type": 3, "heading": 90}],
        [{"type": 4, "heading": 180}, {"type": 2, "heading": 0}, {"type": 4, "heading": 180}, {"type": 4, "heading": 0}, {"type": 2, "heading": 90}],
        [{"type": 3, "heading": 270}, {"type": 1, "heading": 270}, {"type": 1, "heading": 90}, {"type": 1, "heading": 180}, {"type": 1, "heading": 270}]
    ]
}