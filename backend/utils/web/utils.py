import os


def go_up_levels(current_dir, levels):
    for _ in range(levels):
        current_dir = os.path.dirname(current_dir)
    return current_dir
