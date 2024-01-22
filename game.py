import pyxel
import random
import time

class Game:
    def __init__(self):
        pyxel.init(160, 120)

        self.player_x = 75
        self.player_speed = 2
        self.hole_width = 20
        self.wall_y = 0
        self.wall_speed = 1
        self.score = 0
        self.consecutive_scores = 0
        self.game_over = False

        self.slow_down_objects = []

        self.initialize_wall()

        pyxel.run(self.update, self.draw)

    def initialize_wall(self):
        # Initialize wall and hole
        self.hole_x = random.randint(0, pyxel.width - self.hole_width)

    def update(self):
        if self.game_over:
            return

        # Update player input
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 0:
            self.player_x -= self.player_speed
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < pyxel.width - 10:
            self.player_x += self.player_speed

        # Move the wall
        self.wall_y += self.wall_speed
        if self.wall_y > pyxel.height:
            self.wall_y = 0
            self.initialize_wall()
            self.score += 1

            if self.score % 5 == 0:
                # Increase speeds after scoring 5 consecutive points
                self.player_speed += 2
                self.wall_speed += 1
                self.consecutive_scores += 1
            else:
                self.consecutive_scores = 0

            # Generate a random number of slow-down objects after scoring 7 points
            if self.score >= 7 and random.random() < 0.3:
                num_objects = random.randint(1, 3)  # Adjust the range as needed
                for _ in range(num_objects):
                    self.generate_slow_down_object()

        # Check for collision with slow-down objects
        for slow_down_object in self.slow_down_objects:
            if slow_down_object.active and slow_down_object.collides_with_player(self.player_x, pyxel.height - 10):
                self.player_speed = max(1, self.player_speed - 1)
                self.wall_speed = max(1, self.wall_speed - 1)
                slow_down_object.deactivate()

        # Remove inactive slow-down objects
        self.slow_down_objects = [obj for obj in self.slow_down_objects if obj.active]

        # Slow down duration
        for slow_down_object in self.slow_down_objects:
            if slow_down_object.active:
                elapsed_time = time.time() - slow_down_object.activation_time
                remaining_time = max(0, 7 - elapsed_time)
                pyxel.text(pyxel.width - 30, 5, f"Time: {int(remaining_time)}", 7)

        # Check for collision with wall
        if (
            pyxel.height - 10 < self.wall_y + 10 and
            (self.player_x + 10 <= self.hole_x or self.player_x >= self.hole_x + self.hole_width)
        ):
            # Game over condition
            self.game_over = True

        # Reset consecutive scores if the player misses a point
        if self.consecutive_scores > 0 and self.score % 5 != 0:
            self.consecutive_scores = 0

        # Update slow-down objects
        for slow_down_object in self.slow_down_objects:
            slow_down_object.update()

    def draw(self):
        pyxel.cls(0)

        # Draw player
        pyxel.rect(self.player_x, pyxel.height - 10, 10, 10, 9)

        # Draw wall with a wider hole
        pyxel.rect(0, self.wall_y, self.hole_x, 10, 12)
        pyxel.rect(
            self.hole_x + self.hole_width,
            self.wall_y,
            pyxel.width - (self.hole_x + self.hole_width),
            10,
            12,
        )

        # Draw slow-down objects
        for slow_down_object in self.slow_down_objects:
            slow_down_object.draw()

        # Draw score
        pyxel.text(5, 5, f"Score: {self.score}", 7)

        if self.game_over:
            # Display game over label in red text
            pyxel.text(50, 50, "Game Over", 8)

    def generate_slow_down_object(self):
        slow_down_object = SlowDownObject()
        self.slow_down_objects.append(slow_down_object)


class SlowDownObject:
    def __init__(self):
        self.x = random.randint(10, 150)
        self.y = 0
        self.size = 5
        self.active = True
        self.activation_time = time.time()

    def update(self):
        if self.active:
            self.y += 0.5
            if self.y > pyxel.height:
                self.active = False

    def collides_with_player(self, player_x, player_y):
        return (
            player_x < self.x + self.size and
            player_x + 10 > self.x and
            player_y < self.y + self.size and
            player_y + 10 > self.y
        )

    def deactivate(self):
        self.active = False

    def draw(self):
        if self.active:
            pyxel.rect(self.x, self.y, self.size, self.size, 7)


if __name__ == "__main__":
    Game()
