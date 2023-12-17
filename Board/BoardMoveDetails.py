# Expecting: 1 Array chứa những BoardTurnDetails
# Result: There is, which is called: _listMarked, in BasicBoardLogic
class BoardTurnDetails:
    def __init__(self, playerId, pos_x, pos_y):
        # upon each turn, return out playerID and the current board position (without saving it anywhere)
        self.playerId = playerId
        self.position = (pos_x, pos_y)

    def show_details(self):
        print("{} has been reveal at position ({}, {})".format(self.playerId, self.position[0], self.position[1]))


