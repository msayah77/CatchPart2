import pygame, simpleGE, random

""" catch.py 
    slide and catch Demo
    Mohamad
"""

class Ball(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Ball.png")  # Set the ball image
        self.setSize(25, 25)  # Set ball size
        self.minSpeed = 3   # Minimum speed for ball fall
        self.maxSpeed = 8   # Minimum speed for ball fall
        self.reset()
        
    def reset(self):
        #move to top of screen
        self.y = 10
        
        #x is random 0 - screen width
        self.x = random.randint(0, self.screenWidth)
        
        #dy is random minSpeed to maxSpeed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
         # If ball falls below the screen, reset its position
        if self.bottom > self.screenHeight:
            self.reset()


class Basket(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Basket.png")  # Set the basket image
        self.setSize(50, 50)  # Set basket size
        self.position = (320, 400)  # Set initial basket position
        self.moveSpeed = 5    # Set speed for moving the basket
        
    def process(self):
        # Move basket left or right 
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"  # Initialize score text
        self.center = (100, 30)  # Position the score label
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"  # Initialize time label
        self.center = (500, 30)  # Position the time label
    
 
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("hall.jpg")  # Set the background image
        
        self.sndBalls = simpleGE.Sound("pickupCoin.wav") # Sound when ball hit the basket
        self.numBalls = 10  # Number of balls in the game
        self.score = 0
        self.lblScore = LblScore()

        self.timer = simpleGE.Timer() # Game timer
        self.timer.totalTime = 10  # Set total game time to 10 seconds
        self.lblTime = LblTime()
        
        self.basket = Basket(self)
        
        self.balls = []
        for i in range(self.numBalls):
            self.balls.append(Ball(self))   # Add balls to the game
            
        self.sprites = [self.basket, 
                        self.balls,
                        self.lblScore,
                        self.lblTime]   # List of sprites
        
    def process(self):
        for ball in self.balls:        
            if self.basket.collidesWith(ball):
                self.sndBalls.play()   # Play sound when ball is hit into the basket
                ball.reset()
                self.score += 1   # Increase score by 1
                self.lblScore.text = f"Score: {self.score}"   # Update score label
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        # If time is up, print final score and stop the game
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()

        self.prevScore = prevScore  # Set previous score

        self.setImage("hall.jpg")
        self.response = "Quit"
        
        # Game instructions text
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are the team's star player!", 
        "Move with left and right arrow keys.",
        "Catch as much balls as you can",
        "in the time provided",
        "",
        "Good luck!"]
        
         # Position instructions label
        self.directions.center = (320, 200)
        self.directions.size = (500, 250)
        
         # Play and Quit buttons
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        # Show the last score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last score: {self.prevScore}" # Update last score text

        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()


def main():
    
    keepGoing = True
    lastScore = 0

    while keepGoing:
         # Show instructions scene and wait for user input
        instructions = Instructions(lastScore)
        instructions.start()
        
         # If user clicks Play, start the game
        if instructions.response == "Play":    
            game = Game()
            game.start()
            lastScore = game.score
            
        # If user clicks Quit, stop the loop
        else:
            keepGoing = False
            
if __name__ == "__main__":
    main()









