import random
from time import sleep
import pygame
import os

# Get the current working directory and Score file
current_directory = os.getcwd()
score_file_path = os.path.join(os.getcwd(), 'history/scores.txt')
play_car1_path = os.path.join(os.getcwd(), 'img/rolls-royce.png')
player_car2_path = os.path.join(os.getcwd(), 'img/Aston-Martin.png')
player_car3_path = os.path.join(os.getcwd(), 'img/bugatti.png')
enemy_car1_path = os.path.join(os.getcwd(), 'img/police-car2.png')
enemy_car2_path = os.path.join(os.getcwd(), 'img/police-car.png')
enemy_car3_path = os.path.join(os.getcwd(), 'img/police-car.png')
road_1_path = os.path.join(os.getcwd(),'img/dark-yellow2-road.png')
road_2_path = os.path.join(os.getcwd(),'img/dark-yellow2-road.png')
backGround_img_path = os.path.join(os.getcwd(), 'img/')
backGround_sound_path = os.path.join(os.getcwd(), 'sounds/mixkit-game-level-music-689.wav')
crash_sound_path = os.path.join(os.getcwd(), 'sounds/mixkit-truck-crash-with-explosion-1616.wav')

# Connect to Arduino


def read_scores():
    highest_score = 0
    last_score = 0
    with open(score_file_path, "r") as file:
        for line in file:
            # Execute the line as Python code
            exec(line)
            # Capture the variables from the file
            if 'highest_score' in line:
                highest_score = int(line.split('=')[-1])
            elif 'last_score' in line:
                last_score = int(line.split('=')[-1])

    return highest_score, last_score

def save_scores(new_highest_score, new_last_score):
    try:
        with open(score_file_path, "r") as file:
            existing_scores = file.readlines()
            existing_highest_score = int(existing_scores[0].split('=')[-1])
            existing_last_score = int(existing_scores[1].split('=')[-1])
    except FileNotFoundError:
        existing_highest_score = 0
        existing_last_score = 0
    if new_highest_score > existing_highest_score:
        existing_highest_score = new_highest_score
    with open(score_file_path, "w") as file:
        file.write(f"highest_score = {existing_highest_score}\n")
        file.write(f"last_score = {new_last_score}\n")


def scale_car(image_path, target_width=100):
    pygame.init()
    car_image = pygame.image.load(image_path)
    original_width, original_height = car_image.get_rect().size
    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio)
    scaled_car_image = pygame.transform.scale(car_image, (target_width, target_height))
    return scaled_car_image, target_width,target_height


class CarRacing:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.display_width = 1200
        self.display_height = 900
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.crashed = False
        # Locating points
        self.m_right = int(self.display_width * (4 / 5) - 90)
        self.m_left = int(self.display_width * (1 / 5) + 40)
        self.count = 0
        # player car
        self.carImg, self.scaled_car_width, car_height = scale_car(player_car2_path)
        self.car_x_coordinate = (self.display_width * 0.5)
        self.car_y_coordinate = (self.display_height * 0.7)
        # Background
        self.bg_img_height = self.display_height
        self.bg_img_width = int(self.display_width * 3 / 5)
        self.bgImg = pygame.image.load(road_1_path)
        self.bgImg = pygame.transform.scale(self.bgImg, (self.bg_img_width, self.bg_img_height))
        self.bg_speed = 3
        self.bg_x = int(self.display_width * (1 / 5))
        self.bg_y = 0;
        # Enemy Car
        self.enemy_car, self.enemy_car_width, self.enemy_car_height = scale_car(enemy_car1_path)
        self.enemy_car_start_x = random.randrange(self.bg_x, self.m_right)
        self.enemy_car_start_y = -700
        self.enemy_car_speed = 5
        self.crashed = False
        # Locating points
        self.m_right = int(self.display_width * (4 / 5) - 90)
        self.m_left = int(self.display_width * (1 / 5) + 40)
        self.count = 0


        # audios
        pygame.mixer.music.load(backGround_sound_path)
        pygame.mixer.music.play(-1)
        self.crash_sound = pygame.mixer.Sound(crash_sound_path)

        # initializing the screen
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        pygame.mixer.init()


    def menu(self):
        l_high_score,last_score = read_scores()
        menu_font = pygame.font.SysFont("comicsansms", 50)
        white = (255, 255, 255)
        menu_loop = True
        while menu_loop:
            self.gameDisplay.fill((0,0,0))  # Fill the background with black
            menu_text = menu_font.render("Car Dodge", True, white)
            self.gameDisplay.blit(menu_text, (self.display_width * 0.35, self.display_height * 0.2))
            play_text = menu_font.render("1. Play Game", True, white)
            self.gameDisplay.blit(play_text, (self.display_width * 0.35, self.display_height * 0.4))
            quit_text = menu_font.render("2. Quit", True, white)
            self.gameDisplay.blit(quit_text, (self.display_width * 0.35, self.display_height * 0.5))
            high_score_text = menu_font.render(f"High Scores = {l_high_score}", True, white)
            last_score_text = menu_font.render(f"Last Scores = {last_score} ", True, white)
            self.gameDisplay.blit(high_score_text, (self.display_width * 0.35, self.display_height * 0.6))
            self.gameDisplay.blit(last_score_text, (self.display_width * 0.35, self.display_height * 0.7))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.crashed = False
                        menu_loop = False
                    elif event.key == pygame.K_2:
                        print("Goodbye!")
                        pygame.quit()
                        menu_loop = False
    def detect_collisions(self):
        if self.car_y_coordinate < self.enemy_car_start_y + self.enemy_car_height:
            if (
                    self.enemy_car_start_x < self.car_x_coordinate < self.enemy_car_start_x + self.enemy_car_width) or (
                    self.enemy_car_start_x < self.car_x_coordinate + self.scaled_car_width < self.enemy_car_start_x + self.enemy_car_width):
                self.crashed = True
                self.crash_sound.play()
                self.display_message("Game Over U knocked !!!")


        if self.car_x_coordinate < self.m_left or self.car_x_coordinate > self.m_right:
            self.crashed = True
            self.display_message("Game Over !!!")
        save_scores(self.count, self.count)
    def show_background(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y))
        self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y - self.display_height))

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))


    def start_game(self):

        while True:
            self.__init__()
            self.menu()
            while not self.crashed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.car_x_coordinate -= 25
                            print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                        elif event.key == pygame.K_RIGHT:
                            self.car_x_coordinate += 25
                            print ("CAR X COORDINATE: %s" % self.car_x_coordinate)
                        elif event.key == pygame.K_UP:
                            self.car_y_coordinate -= 30  # Move forward
                            print ("CAR Y COORDINAT E: %s" % self.car_y_coordinate)
                        elif self.car_y_coordinate<(self.display_height * 0.78):
                            if event.key == pygame.K_DOWN:
                                self.car_y_coordinate += 30  # Move backward
                                print ("CAR X COORDINATES: %s" % self.car_y_coordinate)
                        print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))

                self.gameDisplay.fill(self.black)
                #Logic to loop load
                self.bg_y += self.bg_speed
                if self.bg_y >= self.display_height:
                    self.bg_y = 0

                self.show_background()
                self.run_enemy_car(self.enemy_car_start_x, self.enemy_car_start_y)
                self.enemy_car_start_y += self.enemy_car_speed

                if self.enemy_car_start_y > self.display_height:
                    self.enemy_car_start_y = 0 - self.enemy_car_height
                    self.enemy_car_start_x = random.randrange(self.m_left, self.m_right)

                self.car(self.car_x_coordinate, self.car_y_coordinate)
                self.highscore(self.count)
                self.count += 1
                self.increase_speed()
                self.detect_collisions()





                pygame.display.update()
                self.clock.tick(60)


    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, self.red)
        self.gameDisplay.blit(text, (self.m_left,self.display_width*1/3))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(2)

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def increase_speed(self):
        if self.count > 5000:
            self .bg_speed = 15
            self.enemy_car_speed = 17
        elif self.count > 4000:
            self.bg_speed = 13
            self.enemy_car_speed = 15
        elif self.count > 3000:
            self.bg_speed = 12
            self.enemy_car_speed = 13.5
        elif self.count > 2000:
            self.bg_speed = 9
            self.enemy_car_speed = 10
        elif self.count > 1000:
            self.bg_speed = 6
            self.enemy_car_speed = 7.5




    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 18)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (self.m_left,self.display_width*2/3))

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.start_game()
