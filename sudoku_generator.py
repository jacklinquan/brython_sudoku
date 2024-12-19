"""Sudoku Generator.

A challenging number of clues is within the range from 17 to 32.
"""

import time
import random
import asyncio

from sudoku_solver import SudokuBoard, SudokuSolver


class SudokuGenerator:
    BEGINNER = 46
    EASY = 40
    MEDIUM = 34
    HARD = 28
    EXPERT = 17

    def __init__(self, seed=None) -> None:
        if seed is not None:
            random.seed(seed)

    def _block_048_or_246(self):
        """Block048: 0, block246: 1

        Blocks:
        0 1 2
        3 4 5
        6 7 8
        """
        return random.choice([0, 1])

    def _set_block_randomly(self, board, b):
        vals = sorted(SudokuBoard.FULL_SET)
        random.shuffle(vals)
        block = [[vals[r * 3 + c] for c in range(3)] for r in range(3)]
        r0, c0 = board.get_position_from_block_num(b)
        for dr in range(3):
            for dc in range(3):
                board.grid[r0 + dr][c0 + dc] = block[dr][dc]

    def generate_solved_board(self):
        board = SudokuBoard("0" * 81)
        if self._block_048_or_246():
            self._set_block_randomly(board, 2)
            self._set_block_randomly(board, 4)
            self._set_block_randomly(board, 6)
        else:
            self._set_block_randomly(board, 0)
            self._set_block_randomly(board, 4)
            self._set_block_randomly(board, 8)
        return SudokuSolver().get_1_solution(board)

    def generate(self, min_clues=17):
        board = self.generate_solved_board()
        solver = SudokuSolver()

        full_list = [(r, c, board.grid[r][c]) for r in range(9) for c in range(9)]
        random.shuffle(full_list)
        num_clues = 81

        while full_list and num_clues > min_clues:
            r, c, val = full_list.pop()
            board.grid[r][c] = 0
            num_clues -= 1
            single_solution, temp = solver.at_most_1_solution(board)
            if not single_solution:
                board.grid[r][c] = val
                num_clues += 1

        return board

    def generate_level(self, level=None):
        if level is None:
            level = self.BEGINNER
        return self.generate(random.randrange(level, level + 4))

    async def async_generate_solved_board(self):
        board = SudokuBoard("0" * 81)
        if self._block_048_or_246():
            self._set_block_randomly(board, 2)
            self._set_block_randomly(board, 4)
            self._set_block_randomly(board, 6)
        else:
            self._set_block_randomly(board, 0)
            self._set_block_randomly(board, 4)
            self._set_block_randomly(board, 8)
        return await SudokuSolver().async_get_1_solution(board)

    async def async_generate(self, min_clues=17):
        board = await self.async_generate_solved_board()
        solver = SudokuSolver()

        full_list = [(r, c, board.grid[r][c]) for r in range(9) for c in range(9)]
        random.shuffle(full_list)
        num_clues = 81

        while full_list and num_clues > min_clues:
            r, c, val = full_list.pop()
            board.grid[r][c] = 0
            num_clues -= 1
            single_solution, temp = await solver.async_at_most_1_solution(board)
            if not single_solution:
                board.grid[r][c] = val
                num_clues += 1

        return board

    async def async_generate_level(self, level=None):
        if level is None:
            level = self.BEGINNER
        return await self.async_generate(random.randrange(level, level + 6))


def test_sudoku_generator():
    for i in range(20):
        board = SudokuGenerator(seed=None).generate_level(level=SudokuGenerator.BEGINNER)
        print(board.get_sdm())
    # print(board.get_num_of_clues())
    # print(board)


async def async_test_sudoku_generator():
    env_dict = {}
    env_dict["end_event"] = asyncio.Event()
    env_dict["sec_count"] = 0

    async def async_count_1s():
        print("Start counting.")
        while not env_dict["end_event"].is_set():
            await asyncio.sleep(1)
            env_dict["sec_count"] += 1
            print(f"{env_dict['sec_count']} s.")

    asyncio.create_task(async_count_1s())

    print()
    print("With asyncio:")
    print()

    board = await SudokuGenerator(seed=None).async_generate_level(
        level=SudokuGenerator.EXPERT
    )
    print(board.get_num_of_clues())
    print(board)

    env_dict["end_event"].set()


if __name__ == "__main__":
    test_sudoku_generator()
    # asyncio.run(async_test_sudoku_generator())
