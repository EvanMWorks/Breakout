######################################################################
# Name: Evan Works
######################################################################

"""
This program (once you have finished it) implements the Breakout game
"""

from pgl import GWindow, GOval, GRect, GLine, GLabel
import random

# Constants
GWINDOW_WIDTH = 360                     # Width of the graphics window
GWINDOW_HEIGHT = 600                    # Height of the graphics window
N_ROWS = 10                              # Number of brick rows
N_COLS = 10                             # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1              # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 1             # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3           # Ratio of brick to paddle width
BRICK_SEP = 2                           # Separation between bricks (in pixels)
TOP_FRACTION = 0.1                      # Fraction of window above bricks
BOTTOM_FRACTION = 0.05                  # Fraction of window below paddle
N_BALLS = 3                             # Number of balls (lives) in a game
TIME_STEP = 10                          # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0                # Starting y velocity downwards
MIN_X_VELOCITY = 1.0                    # Minimum random x velocity
MAX_X_VELOCITY = 3.0                    # Maximum random x velocity

# Derived Constants
BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_X = (GWINDOW_WIDTH - PADDLE_WIDTH)/2
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_DIAMETER = BRICK_WIDTH / BRICK_TO_BALL_RATIO

#First and Last Bricks Distance from Walls WIDTH
SIDE_DISTANCE = (GWINDOW_WIDTH - ((10*BRICK_WIDTH) + (9*BRICK_SEP)))/2
DISTANCE_TOP_BRICKS = GWINDOW_HEIGHT*TOP_FRACTION
gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)

# Function: breakout
def breakout():
    """The main program for the Breakout game."""

    #Defining Variables
    NEW_SIDE_DISTANCE = SIDE_DISTANCE
    NEW_DISTANCE_TOP_BRICKS = DISTANCE_TOP_BRICKS

    #Make Bricks
    for n in range(1, (N_COLS*N_ROWS)+1):
        FIRST_BRICK = GRect(NEW_SIDE_DISTANCE, NEW_DISTANCE_TOP_BRICKS, BRICK_WIDTH, BRICK_HEIGHT)
        if n <= 20:
            FIRST_BRICK.set_fill_color("Red")
            FIRST_BRICK.set_filled(True)
            gw.add(FIRST_BRICK)
        elif n > 20 and n <= 40:
            FIRST_BRICK.set_fill_color("Orange")
            FIRST_BRICK.set_filled(True)
            gw.add(FIRST_BRICK)
        elif n > 40 and n <= 60:
            FIRST_BRICK.set_fill_color("Green")
            FIRST_BRICK.set_filled(True)
            gw.add(FIRST_BRICK)
        elif n > 60 and n <= 80:
            FIRST_BRICK.set_fill_color("Cyan")
            FIRST_BRICK.set_filled(True)
            gw.add(FIRST_BRICK)
        elif n > 80 and n <= 100:
            FIRST_BRICK.set_fill_color("Blue")
            FIRST_BRICK.set_filled(True)
            gw.add(FIRST_BRICK)
        if n % 10 == 0:
            NEW_DISTANCE_TOP_BRICKS += (BRICK_HEIGHT + BRICK_SEP)
            NEW_SIDE_DISTANCE = SIDE_DISTANCE
        else:
            NEW_SIDE_DISTANCE += (BRICK_WIDTH + BRICK_SEP)
    
    
       
    #Make Moving Paddle
       
    PADDLE = GRect(PADDLE_X, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    PADDLE.set_fill_color("Black")
    PADDLE.set_filled(True)
    gw.add(PADDLE)

    
    # Makes Ball
    BALL = GOval((GWINDOW_WIDTH-BALL_DIAMETER)/2, (GWINDOW_HEIGHT-BALL_DIAMETER)/2, BALL_DIAMETER, BALL_DIAMETER)
    BALL.set_fill_color("Black")
    BALL.set_filled(True)
    gw.add(BALL)

    #Moving Ball
    gw.vy= INITIAL_Y_VELOCITY
    gw.vx = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
    if random.uniform(0,1) < 0.5:
        gw.vx = -gw.vx

    #Making Boundaries
    LEFT_LINE = GLine(0, 0, 0, GWINDOW_HEIGHT)
    gw.add(LEFT_LINE)

    RIGHT_LINE = GLine(GWINDOW_WIDTH, 0, GWINDOW_WIDTH, GWINDOW_HEIGHT)
    gw.add(RIGHT_LINE)

    TOP = GLine(0, 0, GWINDOW_WIDTH, 0)
    gw.add(TOP)

    BOTTOM = GLine(0, GWINDOW_HEIGHT, GWINDOW_WIDTH, GWINDOW_HEIGHT)
    gw.add(BOTTOM)


    def drag_action(e):
        if e.get_x() <= GWINDOW_WIDTH - PADDLE_WIDTH:
            if e.get_x() >= 0:
                PADDLE.set_location(e.get_x(), PADDLE_Y)

    gw.add_event_listener("mousemove", drag_action)
    
    #counters
    gw.count = 0
    gw.lives = 3
    
    #End Game Screen
    end_game = GRect(0, 0 , GWINDOW_WIDTH, GWINDOW_HEIGHT)
    end_game.set_fill_color("White")
    end_game.set_filled(True)
    win_message = GLabel("YOU WIN!", GWINDOW_WIDTH/3, GWINDOW_HEIGHT/2)
    win_message.set_font("bold 20pt 'serif'")
    lose_message = GLabel("YOU LOSE :(", GWINDOW_WIDTH/3, GWINDOW_HEIGHT/2)
    lose_message.set_font("bold 20pt 'serif'")

    #step/timer function
    def step():  
        if gw.ball_is_moving == True:
            BALL.move(gw.vx, gw.vy)
            
           

        collider = get_colliding_object()
        if collider != None:

            if collider == PADDLE or collider == TOP:
                gw.vy = -gw.vy

            elif collider == RIGHT_LINE or collider == LEFT_LINE:
                gw.vx = -gw.vx

            elif collider == BOTTOM:
                gw.lives -= 1
                gw.ball_is_moving = False
                BALL.set_location((GWINDOW_WIDTH-BALL_DIAMETER)/2, (GWINDOW_HEIGHT-BALL_DIAMETER)/2)
                
                #Checks Loss
                if gw.lives == 0:
                    timer.stop()
                    gw.add(end_game)
                    gw.add(lose_message)
                    

            elif collider == end_game:
                timer.stop()
                BALL.set_location((GWINDOW_WIDTH-BALL_DIAMETER)/2, (GWINDOW_HEIGHT-BALL_DIAMETER)/2)

            else:
                gw.vy = -gw.vy
                gw.remove(collider)
                gw.count += 1
                
                #Chekcs Win
                if gw.count == (N_COLS*N_ROWS):
                    gw.add(end_game)
                    gw.add(win_message)
                    
                

    timer = gw.set_interval(step, TIME_STEP)

   #makes the ball start moving on a click
    gw.ball_is_moving = False
    def click_action(e):
        gw.ball_is_moving = True

    gw.add_event_listener("click", click_action)

    #finds the object collding into one of the balls corners
    def get_colliding_object():
            
            a = gw.get_element_at(BALL.get_x(), BALL.get_y())
            if a != None:
                return(a)

            b = gw.get_element_at((BALL.get_x())+BALL_DIAMETER, BALL.get_y())
            if b != None:
                return(b)

            c = gw.get_element_at(BALL.get_x(), (BALL.get_y())+BALL_DIAMETER)
            if c != None:
                return(c)
            
            d = gw.get_element_at((BALL.get_x())+BALL_DIAMETER, (BALL.get_y())+BALL_DIAMETER)
            if d != None:
                return(d)


# Startup code
if __name__ == "__main__":
    breakout()
