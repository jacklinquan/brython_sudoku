"""Sudoku Solver.

A challenging number of clues is within the range from 17 to 32.

Blocks:
0 1 2
3 4 5
6 7 8

Example sdm format:
004006079000000602056092300078061030509000406020540890007410920105000000840600100

The string represents this starting sudoku puzzle:
Before solving:
0 0 4   0 0 6   0 7 9
0 0 0   0 0 0   6 0 2
0 5 6   0 9 2   3 0 0

0 7 8   0 6 1   0 3 0
5 0 9   0 0 0   4 0 6
0 2 0   5 4 0   8 9 0

0 0 7   4 1 0   9 2 0
1 0 5   0 0 0   0 0 0
8 4 0   6 0 0   1 0 0

After solving:
2 8 4   1 3 6   5 7 9
9 1 3   7 5 4   6 8 2
7 5 6   8 9 2   3 4 1

4 7 8   9 6 1   2 3 5
5 3 9   2 8 7   4 1 6
6 2 1   5 4 3   8 9 7

3 6 7   4 1 5   9 2 8
1 9 5   3 2 8   7 6 4
8 4 2   6 7 9   1 5 3

Other examples:
016400000200009000400000062070230100100000003003087040960000005000800007000006820
049008605003007000000000030000400800060815020001009000010000000000600400804500390
760500000000060008000000403200400800080000030005001007809000000600010000000003041
000605000003020800045090270500000001062000540400000007098060450006040700000203000
409000705000010000006207800200000009003704200800000004002801500000060000905000406
000010030040070501002008006680000003000302000300000045200500800801040020090020000
080070030260050018000000400000602000390010086000709000004000800810040052050090070
000093006000800900020006100000080053006000200370050000002500040001009000700130000
Hardest:
800000000003600000070090200050007000000045700000100030001000068008500010090000400
"""


import asyncio


class SudokuBoard:
    FULL_SET = {i for i in range(1, 10)}
    EMPTY = 0

    def __init__(self, sdm):
        sdm = "".join(sdm.split())
        self.grid = [[int(sdm[r * 9 + c]) for c in range(9)] for r in range(9)]

    def __repr__(self):
        return self.get_sdm()

    def __str__(self):
        grid_string = ""
        for r, row in enumerate(self.grid):
            row_string = ""
            for c, val in enumerate(row):
                row_string += str(val) + " "
                if c % 3 == 2:
                    row_string += "  "
            grid_string += row_string + "\n"
            if r % 3 == 2:
                grid_string += "\n"

        return grid_string

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            raise ValueError(f"{__value} is not {self.__class__.__name__} instance.")
        return self.get_sdm() == __value.get_sdm()

    def __hash__(self) -> int:
        return hash(self.get_sdm())

    @staticmethod
    def get_block_num_from_position(r, c):
        return r // 3 * 3 + c // 3

    @staticmethod
    def get_position_from_block_num(b):
        r = b // 3 * 3
        c = b % 3 * 3
        return r, c

    def get_possible_set(self, r, c):
        if self.grid[r][c] != self.EMPTY:
            return None

        r_set = {val for val in self.grid[r]}
        c_set = {val for val in [self.grid[r][c] for r in range(9)]}
        block_r = r // 3 * 3  # The starting row number of the block of this point.
        block_c = c // 3 * 3  # The starting column number of the block of this point.
        b_set = {
            self.grid[block_r + r][block_c + c] for r in range(3) for c in range(3)
        }

        possible_set = (
            (self.FULL_SET - r_set) & (self.FULL_SET - c_set) & (self.FULL_SET - b_set)
        ) or None

        return possible_set

    def get_sdm(self):
        return "".join(["".join([str(val) for val in row]) for row in self.grid])

    def get_target_unsolved_point(self):
        target_r = None
        target_c = None
        target_possible_set = None

        for r, c in (
            (r, c) for r in range(9) for c in range(9) if self.grid[r][c] == self.EMPTY
        ):
            possible_set = self.get_possible_set(r, c)
            if possible_set:
                if (None in (target_r, target_c)) or (
                    len(target_possible_set) > len(possible_set)
                ):
                    target_r, target_c = r, c
                    target_possible_set = possible_set

        return target_r, target_c, target_possible_set

    def get_num_of_clues(self):
        return [self.grid[r][c] != 0 for r in range(9) for c in range(9)].count(True)

    def get_difficulty_index(self):
        difficulty = 1
        for r, c in (
            (r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0
        ):
            possible_set = self.get_possible_set(r, c)
            difficulty *= len(possible_set) if possible_set else 1
        return difficulty

    def is_valid(self):
        for r in range(9):
            row_list = [val for val in self.grid[r] if val != self.EMPTY]
            row_set = set(row_list)
            if row_set <= self.FULL_SET and len(row_set) != len(row_list):
                return False

        for c in range(9):
            col_list = [
                self.grid[r][c] for r in range(9) if self.grid[r][c] != self.EMPTY
            ]
            col_set = set(col_list)
            if col_set <= self.FULL_SET and len(col_set) != len(col_list):
                return False

        for b in range(9):
            r0, c0 = self.get_position_from_block_num(b)
            block_list = [
                self.grid[r0 + dr][c0 + dc]
                for dr in range(3)
                for dc in range(3)
                if self.grid[r0 + dr][c0 + dc] != self.EMPTY
            ]
            block_set = set(block_list)
            if block_set <= self.FULL_SET and len(block_set) != len(block_list):
                return False

        return True

    def is_finished(self):
        if str(self.EMPTY) in repr(self):
            return False
        return True

    def is_solved(self):
        if self.is_finished() and self.is_valid():
            return True
        return False

    def copy(self):
        return SudokuBoard(self.get_sdm())


class SudokuSolver:
    def _recur_solve_in_place(self, board, show_step=False):
        """Recursively solve the board in place."""
        if board.is_solved():
            return board

        target_r, target_c, target_possible_set = board.get_target_unsolved_point()
        if None in (target_r, target_c):
            return None

        if show_step:
            print(repr(board))
            print()
            print(board)
            print(target_r, target_c, target_possible_set)
            input()

        for val in target_possible_set:
            board.grid[target_r][target_c] = val
            solution = self._recur_solve_in_place(board, show_step)
            if solution is not None and solution.is_finished():
                return solution
            else:
                board.grid[target_r][target_c] = SudokuBoard.EMPTY

        return None

    def get_1_solution(self, board, show_step=False):
        return self._recur_solve_in_place(board.copy(), show_step)

    def _recur_get_all_solutions(self, board):
        """Recursively get all solutions."""
        if board.is_solved():
            return [board.copy()]

        target_r, target_c, target_possible_set = board.get_target_unsolved_point()
        if None in (target_r, target_c):
            return []

        all_solutions = []
        for val in target_possible_set:
            next_board = board.copy()
            next_board.grid[target_r][target_c] = val
            all_solutions += self._recur_get_all_solutions(next_board)
        return all_solutions

    def get_all_solutions(self, board):
        return self._recur_get_all_solutions(board)

    def _recur_at_most_1_solution(self, board):
        # return (True, 0) or (True, 1) or (False, None)
        if board.is_solved():
            return (True, 1)

        target_r, target_c, target_possible_set = board.get_target_unsolved_point()
        if None in (target_r, target_c):
            return (True, 0)

        solution_count = 0
        for val in target_possible_set:
            next_board = board.copy()
            next_board.grid[target_r][target_c] = val
            res, num = self._recur_at_most_1_solution(next_board)
            if res:
                solution_count += num
                if solution_count > 1:
                    return (False, None)
            else:
                return (False, None)

        return (True, solution_count)

    def at_most_1_solution(self, board):
        return self._recur_at_most_1_solution(board)

    async def _async_recur_solve_in_place(self, board):
        """Recursively solve the board in place."""
        await asyncio.sleep(0)

        if board.is_solved():
            return board

        target_r, target_c, target_possible_set = board.get_target_unsolved_point()
        if None in (target_r, target_c):
            return None

        for val in target_possible_set:
            board.grid[target_r][target_c] = val
            solution = await self._async_recur_solve_in_place(board)
            if solution is not None and solution.is_finished():
                return solution
            else:
                board.grid[target_r][target_c] = SudokuBoard.EMPTY

        return None

    async def async_get_1_solution(self, board):
        return await self._async_recur_solve_in_place(board.copy())

    async def _async_recur_get_all_solutions(self, board):
        """Recursively get all solutions."""
        await asyncio.sleep(0)

        if board.is_solved():
            return [board.copy()]

        target_r, target_c, target_possible_set = board.get_target_unsolved_point()
        if None in (target_r, target_c):
            return []

        all_solutions = []
        for val in target_possible_set:
            next_board = board.copy()
            next_board.grid[target_r][target_c] = val
            all_solutions += await self._async_recur_get_all_solutions(next_board)
        return all_solutions

    async def async_get_all_solutions(self, board):
        return await self._async_recur_get_all_solutions(board)

    async def _async_recur_at_most_1_solution(self, board):
        # return (True, 0) or (True, 1) or (False, None)
        await asyncio.sleep(0)

        if board.is_solved():
            return (True, 1)

        target_r, target_c, target_possible_set = board.get_target_unsolved_point()
        if None in (target_r, target_c):
            return (True, 0)

        solution_count = 0
        for val in target_possible_set:
            next_board = board.copy()
            next_board.grid[target_r][target_c] = val
            res, num = await self._async_recur_at_most_1_solution(next_board)
            if res:
                solution_count += num
                if solution_count > 1:
                    return (False, None)
            else:
                return (False, None)

        return (True, solution_count)

    async def async_at_most_1_solution(self, board):
        return await self._async_recur_at_most_1_solution(board)


def test_sudoku_solver():
    # sdm = """
    #     0 0 4   0 0 6   0 7 9
    #     0 0 0   0 0 0   6 0 2
    #     0 5 6   0 9 2   3 0 0

    #     0 7 8   0 6 1   0 3 0
    #     5 0 9   0 0 0   4 0 6
    #     0 2 0   5 4 0   8 9 0

    #     0 0 7   4 1 0   9 2 0
    #     1 0 5   0 0 0   0 0 0
    #     8 4 0   6 0 0   1 0 0
    # """
    sdm = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"

    board = SudokuBoard(sdm)
    solver = SudokuSolver()

    print("Before solving:")
    print(repr(board))
    print(f"Number of clues: {board.get_num_of_clues()}")
    print(f"Difficulty: {board.get_difficulty_index():e}")
    print()
    print(board)

    solution = solver.get_1_solution(board, show_step=False)

    print("After solving:")
    print(repr(solution))
    print()
    print(solution)

    print("All solutions:")
    print(solver.get_all_solutions(board))
    print()

    print("At most 1 solution:")
    print(solver.at_most_1_solution(board))


async def async_test_sudoku_solver():
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

    sdm = "000008200000000040000000090345800600000050000000046100100000900500010300200000000"
    board = SudokuBoard(sdm)
    solver = SudokuSolver()

    print("Before solving:")
    print(repr(board))
    print(f"Number of clues: {board.get_num_of_clues()}")
    print(f"Difficulty: {board.get_difficulty_index():e}")
    print()
    print(board)

    solution = await solver.async_get_1_solution(board)

    print("After solving:")
    print(repr(solution))
    print()
    print(solution)

    print("All solutions:")
    print(await solver.async_get_all_solutions(board))
    print()

    print("At most 1 solution:")
    print(await solver.async_at_most_1_solution(board))

    env_dict["end_event"].set()


if __name__ == "__main__":
    # test_sudoku_solver()
    asyncio.run(async_test_sudoku_solver())
