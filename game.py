class TicTacToe:
    def __init__(self):
        self.board = self.empty_board()

        self.player_1_key = 1

        self.player_2_key = 2

    def make_move(self, row, col, target) -> bool:
        if 0 <= row < len(self.board) and 0 <= col < len(self.board[row]):
            if not self.board[row][col]:
                self.board[row][col] = target
                return True
        return False

    def check_status(self) -> int:  # 1 = P1 wins, 2 = P2 wins, 0 = Continue, -1 = Draw
        t_board = list(zip(*self.board))  # Used to Calculate Vertical (Taking the Transpose)
        if self.lateral_inspection(self.board, self.player_1_key) or self.lateral_inspection(t_board, self.player_1_key) or self.diagonal_inspection(self.board, self.player_1_key):
            return 1
        if self.lateral_inspection(self.board, self.player_2_key) or self.lateral_inspection(t_board, self.player_2_key) or self.diagonal_inspection(self.board, self.player_2_key):
            return 2
        if self.empty(self.board):
            return -1
        return 0

    def reset_board(self) -> None:
        self.board = self.empty_board()

    @staticmethod
    def empty(board):
        for row in board:
            for element in row:
                if not element:
                    return False
        return True

    @staticmethod
    def empty_board():
        return [[0, 0, 0] for _ in range(3)]

    @staticmethod
    def lateral_inspection(arr, target) -> bool:
        for element in arr:
            if sum(element) == 3*target and len(set(element)) == 1:
                return True
        return False

    @staticmethod
    def diagonal_inspection(board, target) -> bool:
        l_count, r_count = 0, 0
        for i in range(len(board)):
            if board[i][i] == target:
                l_count += 1
            if board[i][len(board) - 1 - i] == target:
                r_count += 1
        if l_count == 3 or r_count == 3:
            return True
        return False


if __name__ == '__main__':
    player_1, player_2 = "O", "X"
    game = TicTacToe()
    game.board = [[1, 2, 2],
                  [1, 2, 2],
                  [2, 1, 1]]

    value = 0
    if value:
        print("True")
    else:
        print("False")





