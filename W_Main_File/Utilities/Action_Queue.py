import collections

action_queue = collections.deque()

"""
value = 1
def a():
    global value
    print(value)
    value = 2
"""

"""
[2, 3, 4, 5, 6, 7, 9, 10]

[2, 3] - [4, 5, 6] - [7, 8, 9]

array<10> {0, 0, 0, ...}
"""
