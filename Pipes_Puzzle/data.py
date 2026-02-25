"""
Dữ liệu các mức Pipes Puzzle (8 level: 0-7).
Mỗi ô là dict {type, heading}; (0,0) ở góc dưới-trái.
type: 1=Dead-end, 2=Straight, 3=Elbow, 4=T-joint.
heading: 0=Đông(>), 90=Nam(v), 180=Tây(<), 270=Bắc(^).
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