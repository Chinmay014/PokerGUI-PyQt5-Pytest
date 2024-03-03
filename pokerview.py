import PyQt5.QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from pokermodel import *
import sys

qt_app = QApplication(sys.argv)


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """

    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()
    for suit in 'HDSC':
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit
            key = (value, suit)
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """This class generates the cards graphics on Tablescene background"""
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: CardModel, card_spacing: int = 250, padding: int = 10):
        super().__init__()
        self.scene = TableScene()
        super().__init__(self.scene)
        self.card_spacing = card_spacing
        self.padding = padding
        self.model = card_model
        #  listening to the signal from __change_cards:
        # Add the cards the first time around to represent the initial state.
        self.__change_cards()
        card_model.new_cards.connect(self.__change_cards)

    def __change_cards(self):  # double underscore indicates that this is a private method
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), repr(card.suit))
            renderer = self.all_cards[graphics_key] if self.model.flipped() else self.back_card
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height() - 2 * self.padding) / 313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding // scale, -self.padding // scale,
                          self.viewport().width() // scale, self.viewport().height() // scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


class PlayerWindow(QGroupBox):
    """A custom widget for a player. Contains player name, cards, money and total bet"""

    def __init__(self, playermodel, gamemodel):
        super().__init__()

        # initialisation
        name_font = QFont()
        name_font.setPointSize(18)
        self.playermodel = playermodel
        self.hand = self.playermodel.hand  # This will draw two cards from the deck
        self.name_label = QLabel("{}".format(self.playermodel.name))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setFont(name_font)
        self.total_money = QLabel("Total Money: {}".format(self.playermodel.total_money))
        self.total_bet_money = QLabel("Betted Money this round: {}".format(self.playermodel.total_bet_money))
        self.raise_text_input = QLineEdit(self)
        self.cards_view = CardView(self.playermodel.hand)
        self.buttons = []
        for b in ["Fold", "Call", "Raise"]:
            button = QPushButton("{}".format(b))
            self.buttons.append(button)
            button.setEnabled(self.playermodel.active)

        # layout
        parent_vbox = QVBoxLayout()
        parent_vbox.addWidget(self.name_label)
        child_hbox = QHBoxLayout()
        child_hbox.addWidget(self.cards_view)
        buttons_vbox = QVBoxLayout()
        buttons_vbox.addWidget(self.total_money)
        buttons_vbox.addWidget(self.total_bet_money)
        buttons_vbox.addWidget(self.buttons[0])
        buttons_vbox.addWidget(self.buttons[1])
        buttons_vbox.addWidget(self.raise_text_input)
        buttons_vbox.addWidget(self.buttons[2])
        child_hbox.addLayout(buttons_vbox)
        parent_vbox.addLayout(child_hbox)
        self.setLayout(parent_vbox)

        # logic
        self.playermodel = playermodel
        self.gamemodel = gamemodel
        # receive all necessary signals
        self.gamemodel.money_changed.connect(self.update_display)

        def reveal_cards():
            self.hand.flipped_cards = False

        self.gamemodel.reveal_all_cards.connect(reveal_cards)

        # in place functions
        self.buttons[0].clicked.connect(gamemodel.fold_bet)
        self.buttons[1].clicked.connect(gamemodel.call_bet)

        def bet_raise():
            raise_amount = self.raise_text_input.text()
            if raise_amount.isdigit():
                gamemodel.raise_bet(int(raise_amount))
                self.raise_text_input.clear()

        self.buttons[2].clicked.connect(bet_raise)

    def update_display(self):
        # change active status
        self.playermodel.toggle_active()
        for button in self.buttons:
            button.setEnabled(self.playermodel.active)
        # flip cards as the move is shifted to the other player
        self.hand.flip()
        self.total_money.setText("Total Money: {}".format(self.playermodel.total_money))
        self.total_bet_money.setText("Betted Money this round: {}".format(self.playermodel.total_bet_money))


class TableWindow(QGroupBox):
    """This window creates the Table View with five cards and a status window to show the pot and bet progress"""

    def __init__(self, tablemodel, gamemodel):
        super().__init__()

        # layout
        pot_font = QFont()
        pot_font.setPointSize(14)
        table_hbox = QHBoxLayout()
        self.gamemodel = gamemodel
        self.tablemodel = tablemodel
        self.table_cards = CardView(self.tablemodel.hand)
        table_hbox.addWidget(self.table_cards)
        gamestate_vbox = QVBoxLayout()
        self.pot_label = QLabel("${} in the Pot".format(self.gamemodel.pot_money))
        self.pot_label.setFont(pot_font)
        gamestate_vbox.addWidget(self.pot_label)
        self.status_window = QPlainTextEdit(self)
        # self.status_window.insertPlainText("Start")
        self.status_window.setFixedWidth(200)
        gamestate_vbox.addWidget(self.status_window)
        table_hbox.addLayout(gamestate_vbox)
        self.setLayout(table_hbox)

        # logic, control, signal
        self.gamemodel.pot_money_changed.connect(self.update_pot)
        self.gamemodel.text_changed.connect(self.update_table_display)

    def update_pot(self):
        self.pot_label.setText("${} in the Pot".format(self.gamemodel.pot_money))

    def update_table_display(self, message):
        self.status_window.appendPlainText(message)


class GameWindow(QGroupBox):
    """The parent game window. Contains the player windows and the Table window"""

    def __init__(self, gamemodel):
        super().__init__("Texas Hold'em")
        self.setAlignment(100)

        # initialisation
        self.gamemodel = gamemodel

        # layout
        game_vbox = QVBoxLayout()
        players_hbox = QHBoxLayout()

        self.p1_window = PlayerWindow(self.gamemodel.playermodels[0], self.gamemodel)
        # flip p1 cards to begin with
        self.p1_window.playermodel.hand.flip()
        self.p2_window = PlayerWindow(self.gamemodel.playermodels[1], self.gamemodel)
        players_hbox.addWidget(self.p1_window)
        players_hbox.addWidget(self.p2_window)
        game_vbox.addLayout(players_hbox)

        self.table_window = TableWindow(self.gamemodel.tablemodel, self.gamemodel)
        game_vbox.addWidget(self.table_window)
        self.setLayout(game_vbox)
        self.setGeometry(200, 200, 1600, 800)

        # logic
        self.gamemodel.game_message.connect(self.terminate_window)

    def terminate_window(self, text):
        # pop up message asking user to either quit or restart
        box = QMessageBox()
        box.setText(text)
        box.setWindowTitle("Game Over!")

        restart_game_button = box.addButton("Restart Game", box.YesRole)
        exit_game_button = box.addButton("Exit Game", box.NoRole)

        restart_game_button.clicked.connect(self.gamemodel.restart_game)
        exit_game_button.clicked.connect(self.exit_game)

        box.exec_()

    @staticmethod
    def exit_game():
        sys.exit(qt_app.exec())
