import random
from typing import Union


class Game:
    def __init__(self):
        self.player: Union[str, None] = "Player"
        self.player_score: int = 0
        self.cpu_score: int = 0
        self.is_active: bool = True

    def add_player(self, player) -> None:
        self.player = player

    def get_item(self, n: Union[str, None]) -> str:
        selection = random.randint(1, 3)
        if n:
            selection = n

        if selection == 1:
            return "rock"
        elif selection == 2:
            return "paper"
        elif selection == 3:
            return "scissors"
        else:
            return "exit"

    def tie(self) -> None:
        print("It's a tie.")

    def player_win(self) -> None:
        print("You win!")
        self.player_score += 1

    def cpu_win(self) -> None:
        print("CPU win :(")
        self.cpu_score += 1

    def play(self) -> None:
        while self.is_active:
            print("\nSelect 1 for rock, 2 for paper, 3 for scissors, 0 to exit")
            choice = self.get_item(int(input()))
            cpu_choice = self.get_item()
            if choice == "rock":
                if cpu_choice == "rock":
                    self.tie()
                elif cpu_choice == "paper":
                    self.cpu_win()
                elif cpu_choice == "scissors":
                    self.player_win()
            elif choice == "paper":
                if cpu_choice == "rock":
                    self.player_win()
                elif cpu_choice == "paper":
                    self.tie()
                elif cpu_choice == "scissors":
                    self.cpu_win()
            elif choice == "scissors":
                if cpu_choice == "rock":
                    self.cpu_win()
                elif cpu_choice == "paper":
                    self.player_win()
                elif cpu_choice == "scissors":
                    self.tie()
            elif choice == "exit":
                self.is_active = False
            else:
                self.is_active = False

        output = (
            f"WON: You won {self.player_score} times, CPU won {self.cpu_score} times"
        )
        if self.cpu_score > self.player_score:
            output = f"LOST: CPU won {self.cpu_score} times, you won {self.player_score} times"
        if self.cpu_score == self.player_score:
            output = "The game ended in a tie"
        print("\n" + output)

    def play_round(self, choice):
        cpu_choice = self.get_item(None)
        result = ""

        if choice == "rock":
            if cpu_choice == "rock":
                result = "tie"
            elif cpu_choice == "paper":
                result = "cpu_win"
                self.cpu_win()
            elif cpu_choice == "scissors":
                result = "player_win"
                self.player_win()
        elif choice == "paper":
            if cpu_choice == "rock":
                result = "player_win"
                self.player_win()
            elif cpu_choice == "paper":
                result = "tie"
            elif cpu_choice == "scissors":
                result = "cpu_win"
                self.cpu_win()
        elif choice == "scissors":
            if cpu_choice == "rock":
                result = "cpu_win"
                self.cpu_win()
            elif cpu_choice == "paper":
                result = "player_win"
                self.player_win()
            elif cpu_choice == "scissors":
                result = "tie"
        elif choice == "exit":
            self.is_active = False
            self.player = None
            result = "exit"

        return {
            "player_choice": choice,
            "cpu_choice": cpu_choice,
            "result": result,
            "player_score": self.player_score,
            "cpu_score": self.cpu_score,
        }


if __name__ == "__main__":
    game = Game()
    print("Welcome to the game of Rock-Paper-Scissors!")
    player = input("Enter player: ")
    game.add_player(player.strip())
    game.play()
