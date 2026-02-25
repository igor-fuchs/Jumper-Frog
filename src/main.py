"""Entry point for Jumper Frog."""

from src.game import Game


def main() -> None:
    """Create and run the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
