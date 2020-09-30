import arcade  # For GUI and animation
import random  # For choosing initial ball velocity
import pyglet  # For centering the window
import datetime

# Pyglet methods to fetch monitor resolution. This was added after I realised Windows scaling messes with resolutions
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
date = datetime.datetime.today().strftime('%d-%m-%Y')
time_started = datetime.datetime.today().strftime("%H:%M")

# Constants to be used in the program
BOUNCINESS = 1.05  # This means the ball gets 5% faster every time it hits a paddle
MONITOR_WIDTH = screen.width  # Uses the Pyglet get_default_screen method to find the monitor width
MONITOR_HEIGHT = screen.height  # Uses the same Pyglet methods to find the height

# Constants. Use of conversion factors so that the window size is consistent across any monitor/device
SCREEN_WIDTH = int(MONITOR_WIDTH * 0.65)
SCREEN_HEIGHT = int(MONITOR_HEIGHT * 0.81)
print("Monitor Resolution:\n{}x{}\n".format(SCREEN_WIDTH, SCREEN_HEIGHT))
player1name = ""
player2name = ""

# List of images that say 0, 1, 2 etc. Uses the original Pong font
points = [arcade.load_texture("images/Number0.png"),
          arcade.load_texture("images/Number1.png"),
          arcade.load_texture("images/Number2.png"),
          arcade.load_texture("images/Number3.png"),
          arcade.load_texture("images/Number4.png"),
          arcade.load_texture("images/Number5.png"),
          arcade.load_texture("images/Number6.png"),
          arcade.load_texture("images/Number7.png"),
          arcade.load_texture("images/Number8.png"),
          arcade.load_texture("images/Number9.png")]

# List of end game screens. Depends on who won
win_textures = [arcade.load_texture("images/Player1Wins.png"), arcade.load_texture("images/Player2Wins.png")]


class Ball:
    """
    Contains the methods to create the balls.Use of a class allows us to track the properties of the ball, making it easier to animate
    and create collision physics.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.radius = 0
        self.colour = arcade.color.WHITE

    def reset_position(self):
        """
        This centres the ball to the centre of the screen, and sets the speed to 0
        """
        self.x = SCREEN_WIDTH // 2  # The position of the ball on the horizontal axis
        self.y = SCREEN_HEIGHT // 2  # The position of the ball on the vertical axis
        self.change_x = 0  # How quickly the ball moves left or right (measured in pixels per second)
        self.change_y = 0  # Same as above but for up and down

    def start_moving(self):
        if self.change_x == 0 and self.change_y == 0:
            self.change_x = random.choice([-400, 400])  # Chooses whether the ball starts moving left or right
            self.change_y = random.choice([-300, 300])  # Chooses whether the ball starts moving up or down
            # The change_y is less than change_x so that the ball movement isn't as predictable.


class Paddle:
    """
    This class is created for the sole purpose of tracking the position of the paddles, and to make
    it possible to control by the user
    """

    def __init__(self):
        self.x = 40
        self.y = SCREEN_HEIGHT // 2
        self.change_y = 0
        self.height = 80
        self.width = 10
        self.colour = arcade.color.WHITE


# Self-explanatory, creates the ball and centres it to the centre of the screen
def make_ball():
    ball = Ball()
    ball.x = SCREEN_WIDTH // 2
    ball.y = SCREEN_HEIGHT // 2
    ball.change_x = 0
    ball.change_y = 0
    ball.radius = 10

    return ball


def make_paddles():
    paddle1 = Paddle()
    paddle2 = Paddle()
    paddle2.x = SCREEN_WIDTH - 40
    return paddle1, paddle2


class MyGame(arcade.Window):
    """
    Main Class. This is a "special" class in that it overrides arcade's own classes so that it is easier to animate
    on-screen objects.
    """

    def __init__(self, width, height):
        super().__init__(width, height, "Pong - By Danyal Durrani")

        arcade.set_background_color(arcade.color.BLACK)
        self.set_location(MONITOR_WIDTH // 2 - SCREEN_WIDTH // 2, MONITOR_HEIGHT // 2 - SCREEN_HEIGHT // 2)
        self.ball = make_ball()
        self.ball_list = []
        self.ball_list.append(self.ball)
        self.game_finished = False

        self.paddles = make_paddles()
        self.paddle1 = self.paddles[0]
        self.paddle2 = self.paddles[1]
        self.player1points = 0
        self.player2points = 0
        self.player1points_texture = ""
        self.player2points_texture = ""
        self.win_texture = ""
        self.scale = 0.3
        self.restart_init = False
        self.report_written = False
        self.fps = 0
        self.frames = 0

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        arcade.draw_text(str(self.fps), 0.97 * SCREEN_WIDTH, 0.97 * SCREEN_HEIGHT, arcade.color.WHITE, 20)

        if not self.game_finished:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 5, SCREEN_HEIGHT, (46, 46, 46))

            for ball in self.ball_list:
                arcade.draw_circle_filled(ball.x, ball.y, ball.radius, ball.colour)

            for paddle in self.paddles:
                arcade.draw_rectangle_filled(paddle.x, paddle.y, paddle.width, paddle.height, paddle.colour)

            self.player1points_texture = points[self.player1points]
            self.player2points_texture = points[self.player2points]

            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, self.player1points_texture.width * self.scale, self.player1points_texture.height * self.scale, self.player1points_texture)
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT - 50, self.player2points_texture.width * self.scale, self.player2points_texture.height * self.scale, self.player2points_texture)

        if self.player1points == 9:
            self.win_texture = win_textures[0]
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.win_texture.width, self.win_texture.height, self.win_texture)
            self.game_finished = True
            if not self.report_written:
                with open("Results.txt", "a") as f:
                    f.write("\n{} vs {} on {} at {}. {} won with a score of {} - {}.".format(player1name, player2name, date,
                                                                                             time_started, player1name, self.player1points,
                                                                                             self.player2points))
                    self.report_written = True

        if self.player2points == 9:
            self.win_texture = win_textures[1]
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.win_texture.width, self.win_texture.height, self.win_texture)
            self.game_finished = True
            if not self.report_written:
                with open("Results.txt", "a") as f:
                    f.write("\n{} vs {} on {} at {}. {} won with a score of {} - {}.".format(player1name, player2name, date,
                                                                                             time_started, player2name, self.player1points,
                                                                                             self.player2points))
                    self.report_written = True

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.

        delta_time is 1 divided by the FPS we want. It is used so that if there are frame drops, the ball doesn't glitch
        or 'rubber-band' irregularly. This means that it optimises performance for low end system. Makes it easier to
        predict where the ball is. 1/60 is used as most displays go up to 60Hz and using a higher value would require
        more processing power, negating the benefits of this
        """
        self.frames += 1

        if self.frames % 5 == 0:
            self.fps = round(1/delta_time)
        if not self.game_finished:
            for paddle in self.paddles:
                paddle.y += paddle.change_y * delta_time

            for ball in self.ball_list:
                ball.x += ball.change_x * delta_time
                ball.y += ball.change_y * delta_time

                # Checks if the ball has hit the paddles, so that the ball can bounce back
                if ball.x <= 60 and ball.y > self.paddle1.y - (self.paddle1.height // 2) - 15 and ball.y < self.paddle1.y + (self.paddle1.height // 2) + 15:
                    if ball.x > 45:
                        if ball.change_x * BOUNCINESS <= 750:
                            ball.change_x = abs(ball.change_x * BOUNCINESS)
                        else:
                            ball.change_x = abs(ball.change_x)

                if ball.x >= SCREEN_WIDTH - 60 and ball.y > self.paddle2.y - (self.paddle2.height // 2) - 15 and ball.y < self.paddle2.y + (self.paddle2.height // 2) + 15:
                    if ball.x < SCREEN_WIDTH - 45:
                        if ball.change_x * BOUNCINESS >= -750:
                            ball.change_x = abs(ball.change_x * BOUNCINESS) * -1
                        else:
                            ball.change_x = abs(ball.change_x) * -1

                # Checks if the ball has hit the edge, if so then a point is added
                if ball.x < ball.radius:
                    ball.reset_position()
                    self.player2points += 1
                    for paddle in self.paddles:
                        paddle.y = SCREEN_HEIGHT // 2
                if ball.x > SCREEN_WIDTH - ball.radius:
                    ball.reset_position()
                    self.player1points += 1
                    for paddle in self.paddles:
                        paddle.y = SCREEN_HEIGHT // 2

                # This enables the ball to bounce of the top and bottom of the window
                if ball.y < ball.radius + 2:
                    ball.change_y = 300
                if ball.y > SCREEN_HEIGHT - ball.radius - 2:
                    ball.change_y = -300

                # Stops the paddles if they hit the top or bottom
                if self.paddle1.y > SCREEN_HEIGHT - (self.paddle1.height // 2):
                    self.paddle1.change_y = 0
                    self.paddle1.y = SCREEN_HEIGHT - (self.paddle1.height // 2) - 3
                if self.paddle1.y < self.paddle1.height // 2:
                    self.paddle1.change_y = 0
                    self.paddle1.y = self.paddle1.height // 2 + 3

                if self.paddle2.y > SCREEN_HEIGHT - (self.paddle2.height // 2):
                    self.paddle2.change_y = 0
                    self.paddle2.y = SCREEN_HEIGHT - (self.paddle2.height // 2) - 3
                if self.paddle2.y < self.paddle2.height // 2:
                    self.paddle2.change_y = 0
                    self.paddle2.y = self.paddle2.height // 2 + 3

                # Initialises the game after a restart
                if self.restart_init:
                    self.paddle1.y = SCREEN_HEIGHT // 2
                    self.paddle2.y = SCREEN_HEIGHT // 2
                    self.restart_init = False

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        119 = W         115 = S         65362 = UP          65364 = DOWN        32 = SPACE      65479 = F10
        65365 = Page Up         65366 = Page Down
        """
        if key == 119:
            self.paddle1.change_y = 500
        if key == 115:
            self.paddle1.change_y = -500
        if key == 65362 or key == 65365:
            self.paddle2.change_y = 500
        if key == 65364 or key == 65366:
            self.paddle2.change_y = -500
        if key == 32:
            for ball in self.ball_list:
                ball.start_moving()
        if key == 65479:
            self.game_finished = False
            self.restart_init = True
            self.player1points = 0
            self.player2points = 0

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if (key == 119 and self.paddle1.change_y > 0) or (key == 115 and self.paddle1.change_y < 0):
            self.paddle1.change_y = 0
        if (key in [65362, 65365] and self.paddle2.change_y > 0) or (key in [65364, 65366] and self.paddle2.change_y < 0):
            self.paddle2.change_y = 0


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

main()
0