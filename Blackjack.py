# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

# constants for drawing
TITLE_POS = [50, 50]
SCORE_POS = [400, 50]
DEALER_TEXT_POS = [50, 150]
OUTCOME_POS = [300, 150]
DEALER_HAND_POS = [50, 200]
PLAYER_TEXT_POS = [50, 400]
MESSAGE_POS = [300, 400]
PLAYER_HAND_POS = [50, 450]


# helper functions
def update_dealer_text():
    global dealer_text
    dealer_text = "Dealer"
    if not in_play:
        dealer_text += ": " + str(dealer_hand.get_value())


def update_player_text():
    global player_text
    player_text = "Player: " + str(player_hand.get_value())


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card:", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = "["
        for i in range(len(self.cards) - 1):
            s += str(self.cards[i]) + ", "
        if len(self.cards) > 0:
            s += str(self.cards[-1])
        s += "] Value: " + str(self.get_value())
        return s

    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        total_value = 0
        ace = False
        for c in self.cards:
            card_rank = c.get_rank()
            card_value = VALUES[card_rank]
            total_value += card_value
            if card_rank == 'A':
                ace = True
        if ace and (total_value + 10 <= 21):
            return total_value + 10
        return total_value

    def busted(self):
        return self.get_value() > 21

    def draw(self, canvas, p):
        pos = list(p)
        for c in self.cards:
            c.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 20


# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        s = "["
        for i in range(len(self.cards) - 1):
            s += str(self.cards[i]) + ", "
        if len(self.cards) > 0:
            s += str(self.cards[-1])
        s += "]"
        return s


# define event handlers for buttons
def deal():
    global outcome, message, in_play, score
    if in_play:
        score -= 1
    outcome = ""
    message = "Hit or stand?"
    in_play = True

    global deck, player_hand, dealer_hand
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    update_player_text()
    update_dealer_text()

    # print "Player hand: ", player_hand
    # print "Dealer hand: ", dealer_hand


def hit():
    global outcome, message, in_play, score
    if in_play:
        player_hand.add_card(deck.deal_card())
        update_player_text()
        if player_hand.busted():
            outcome = "Player has busted"
            in_play = False
            message = "New deal?"
            score -= 1
            update_dealer_text()
        #    print "Busted"
        # else:
        #    print "Player hand: ", player_hand 


def stand():
    global outcome, message, in_play, score
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            # print "Dealer hand: ", dealer_hand
            if dealer_hand.busted():
                outcome = "Dealer has busted"
                message = "New deal?"
                score += 1
                update_dealer_text()
                # print "Dealer busted"
                return
        if dealer_hand.get_value() < player_hand.get_value():
            outcome = "Player wins!"
            score += 1
            # print "Player wins!"
        else:
            outcome = "Dealer wins!"
            score -= 1
            # print "Dealer wins!"
        update_dealer_text()
        message = "New deal?"


# draw handler
def draw(canvas):
    canvas.draw_text("Blackjack", TITLE_POS, 36, "Blue")
    canvas.draw_text("Score " + str(score), SCORE_POS, 24, "Black")
    canvas.draw_text(dealer_text, DEALER_TEXT_POS, 24, "Black")
    canvas.draw_text(message, MESSAGE_POS, 24, "Black")
    dealer_hand.draw(canvas, DEALER_HAND_POS)
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [DEALER_HAND_POS[0] + CARD_BACK_CENTER[0], DEALER_HAND_POS[1] + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)
    canvas.draw_text(player_text, PLAYER_TEXT_POS, 24, "Black")
    canvas.draw_text(outcome, OUTCOME_POS, 24, "Black")
    player_hand.draw(canvas, PLAYER_HAND_POS)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()
