from pokerview import *

# User can enter inputs here
starting_money = 50000
Player_1_name = "P1"
Player_2_name = "P2"

game_players = [PlayerModel(Player_1_name, starting_money),
                PlayerModel(Player_2_name, starting_money)]
game_table = TableModel()
poker_game = GameModel(game_players, game_table)

qt_app = QApplication(sys.argv)
win = GameWindow(poker_game)
win.show()
qt_app.exec_()
