# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
#           __________                                                      #
#    __  __/ ____/ __ \__ __   This file is part of byron v4!2.0         #
#   / / / / / __/ /_/ / // /   A versatile evolutionary optimizer & fuzzer  #
#  / /_/ / /_/ / ____/ // /_   https://github.com/microgp/byron          #
#  \__  /\____/_/   /__  __/                                                #
#    /_/ --byron-- /_/      You don't need a big goal, be μ-ambitious!   #
#                                                                           #
#############################################################################
# Copyright 2022-2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# Library imports
import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Drawing With Loops Example"


def draw_background():
    """
    This function draws the background. Specifically, the sky and ground.
    """
    # Draw the sky in the top two-thirds
    arcade.draw_rectangle_filled(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3, SCREEN_WIDTH - 1, SCREEN_HEIGHT * 2 / 3, arcade.color.SKY_BLUE
    )

    # Draw the ground in the bottom third
    arcade.draw_rectangle_filled(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6, SCREEN_WIDTH - 1, SCREEN_HEIGHT / 3, arcade.color.DARK_SPRING_GREEN
    )


def draw_bird(x, y):
    """
    Draw a bird using a couple arcs.
    """
    arcade.draw_arc_outline(x, y, 20, 20, arcade.color.BLACK, 0, 90)
    arcade.draw_arc_outline(x + 40, y, 20, 20, arcade.color.BLACK, 90, 180)


def draw_pine_tree(center_x, center_y):
    """
    This function draws a pine tree at the specified location.

    Args:
      :center_x: x position of the tree center.
      :center_y: y position of the tree trunk center.
    """
    # Draw the trunkcenter_x
    arcade.draw_rectangle_filled(center_x, center_y, 20, 40, arcade.color.DARK_BROWN)

    tree_bottom_y = center_y + 20

    # Draw the triangle on top of the trunk
    point_list = ((center_x - 40, tree_bottom_y), (center_x, tree_bottom_y + 100), (center_x + 40, tree_bottom_y))

    arcade.draw_polygon_filled(point_list, arcade.color.DARK_GREEN)


def main():
    """
    This is the main program.
    """

    # Open the window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Start the render process. This must be done before any drawing commands.
    arcade.start_render()

    # Call our drawing functions.
    draw_background()

    # Loop to draw ten birds in random locations.
    for bird_count in range(10):
        # Any random x from 0 to the width of the screen
        x = random.randrange(0, SCREEN_WIDTH)

        # Any random y from in the top 2/3 of the screen.
        # No birds on the ground.
        y = random.randrange(SCREEN_HEIGHT // 3, SCREEN_HEIGHT - 20)

        # Draw the bird.
        draw_bird(x, y)

    # Draw the top row of trees
    for x in range(45, SCREEN_WIDTH, 90):
        draw_pine_tree(x, SCREEN_HEIGHT / 3)

    # Draw the bottom row of trees
    for x in range(65, SCREEN_WIDTH, 90):
        draw_pine_tree(x, (SCREEN_HEIGHT / 3) - 120)

    # Finish the render.
    # Nothing will be drawn without this.
    # Must happen after all draw commands
    arcade.finish_render()

    # Keep the window up until someone closes it.
    arcade.run()


if __name__ == "__main__":
    main()
