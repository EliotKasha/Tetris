class Orientations:
    def __init__(self):
        self.orientations = [[],  # Null to shift index by one

        # Z
        [
            [
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 1, 0, 0],
                [1, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        ],

        # S
        [
            [
                [0, 2, 2, 0],
                [2, 2, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 2, 0, 0],
                [0, 2, 2, 0],
                [0, 0, 2, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 0, 0],
                [0, 2, 2, 0],
                [2, 2, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [2, 0, 0, 0],
                [2, 2, 0, 0],
                [0, 2, 0, 0],
                [0, 0, 0, 0]
            ]
        ],

        # J
        [
            [
                [3, 0, 0, 0],
                [3, 3, 3, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 3, 3, 0],
                [0, 3, 0, 0],
                [0, 3, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 0, 0],
                [3, 3, 3, 0],
                [0, 0, 3, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 3, 0, 0],
                [0, 3, 0, 0],
                [3, 3, 0, 0],
                [0, 0, 0, 0]
            ]
        ],

        # L
        [
            [
                [0, 0, 4, 0],
                [4, 4, 4, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 4, 0, 0],
                [0, 4, 0, 0],
                [0, 4, 4, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 0, 0],
                [4, 4, 4, 0],
                [4, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [4, 4, 0, 0],
                [0, 4, 0, 0],
                [0, 4, 0, 0],
                [0, 0, 0, 0]
            ]
        ],

        # 0
        [
            [
                [0, 5, 5, 0],
                [0, 5, 5, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 5, 5, 0],
                [0, 5, 5, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 5, 5, 0],
                [0, 5, 5, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 5, 5, 0],
                [0, 5, 5, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        ],

        # T
        [
            [
                [0, 6, 0, 0],
                [6, 6, 6, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 6, 0, 0],
                [0, 6, 6, 0],
                [0, 6, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 0, 0],
                [6, 6, 6, 0],
                [0, 6, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 6, 0, 0],
                [6, 6, 0, 0],
                [0, 6, 0, 0],
                [0, 0, 0, 0]
            ]
        ],

        # I
        [
            [
                [0, 0, 0, 0],
                [7, 7, 7, 7],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],

            [
                [0, 0, 7, 0],
                [0, 0, 7, 0],
                [0, 0, 7, 0],
                [0, 0, 7, 0]
            ],

            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [7, 7, 7, 7],
                [0, 0, 0, 0]
            ],

            [
                [0, 7, 0, 0],
                [0, 7, 0, 0],
                [0, 7, 0, 0],
                [0, 7, 0, 0]
            ]
        ],

        ]

        self.kickscw = [
            [[0, -1], [1, -1], [-2, 0], [-2, -1]],
            [[0, -1], [-1, -1], [2, 0], [2, -1]],
            [[0, 1], [1, 1], [-2, 0], [-2, 1]],
            [[0, 1], [-1, 1], [2, 0], [2, 1]]
        ]

        self.kicksccw = [
            [[0, 1], [1, 1], [-2, 0], [-2,  1]],
            [[0, -1], [-1, -1], [2, 0], [2, -1]],
            [[0, -1], [1, -1], [-2, 0], [-2, -1]],
            [[0, 1], [-1, 1], [2, 0], [2, 1]]
        ]