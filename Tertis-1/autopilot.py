"""
TERTIS Autopilot
Player simulation for the Tertis app.
When run, this program will simulate a player of the Tertis app
by interacting with the Tertis API and executing configured strategies.
"""

from TertisApi import TertisApi
from TertisPlayerStrategies import StraightDown


class Player:
    """Simulate a Tertis Player.
    This class represents an instance of a Player of Tertis.
    It is designed to interface with the API of the Tertis program by
    allowing multiple strategies for playing the game to be run against it.
    """

    def __init__(self, strategy=None):
        """Initialize an instance of the Tertis Player class."""
        TertisApi.startGame()


if __name__ == '__main__':
    """Run the autopilot."""
    player = Player(strategy=StraightDown)