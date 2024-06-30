"""
Sprite Sample Program

- This is an alternative evolution of the coin_collector_moving1 game
- This time the coins bounce off the edges of the screen
- This is handled by the Coin class update function, by using the same logic as was used for the
  bouncing balls in a previous program
- Note this time we use .left .right .top .bottom sprite attributes which saves us having to worry about object radius
  for calculating when an object is touching the edge
- In this program we don't respawn collected coins
- As an extra feature we make the coins spin - it is handled the same way as x/y change rate
"""

import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_SWORD = 0.1
SPRITE_SCALING_ENEMY = 0.6

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Enemy(arcade.Sprite):

    def __init__(self, image_file, scale, bullet_list, time_between_firing):

        super().__init__(image_file, scale)

        self.change_x = 0
        self.change_y = 0

        # How long has it been since we last fired?
        self.time_since_last_firing = 0.0

        # How often do we fire?
        self.time_between_firing = time_between_firing

        # When we fire, what list tracks the bullets?
        self.bullet_list = bullet_list

    def on_update(self, delta_time: float = 1 / 60) -> None:

        # Move the enemy
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1

        # Track time since we last fired
        self.time_since_last_firing += delta_time

        # If we are past the firing time, then fire
        if self.time_since_last_firing >= self.time_between_firing:
            # Reset timer
            self.time_since_last_firing = 0

            # Fire the bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
            bullet.center_x = self.center_x
            bullet.angle = -90
            bullet.top = self.bottom
            bullet.change_y = -2
            self.bullet_list.append(bullet)


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None
        self.sword_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self, delta_time):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from builtins
        self.player_sprite = arcade.Sprite("Shelly_Skin-Caribou.png", SPRITE_SCALING_PLAYER)
        self.sword_sprite = arcade.Sprite("iron-sword-skyrim-wiki-14.png", SPRITE_SCALING_SWORD)
        self.player_sprite.center_x = 50
        self.sword_sprite.center_x = 70
        self.player_sprite.center_y = 50
        self.sword_sprite.center_y = 120
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.sword_sprite)



        # Create the enemy instance
        # enemy image from kenney.nl
        zombie = Enemy("zombie_fall.png", SPRITE_SCALING_ENEMY, scale=0.5,
                            bullet_list=self.bullet_list,
                            time_between_firing=2.0)

        # Position the coin
        zombie.center_x = random.randrange(SCREEN_WIDTH)
        zombie.center_y = random.randrange(SCREEN_HEIGHT)
        zombie.change_x = random.randrange(-3, 4)
        zombie.change_y = random.randrange(-3, 4)
        zombie.spin_rate = random.randrange(-3, 4)

        # Add the coin to the lists
        self.enemy_list.append(zombie)

    def on_draw(self,delta_time):
        """ Draw everything """
        arcade.start_render()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # Call on_update for each enemy in  the list
        self.enemy_list.on_update(delta_time)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y
        self.sword_sprite.center_x = x+20
        self.sword_sprite.center_y = y+70


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.enemy_list.on_update(delta_time)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.enemy_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for enemy in hit_list:
            enemy.remove_from_sprite_lists()
            self.score += 1


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
