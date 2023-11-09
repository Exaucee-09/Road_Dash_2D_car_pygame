import random
from time import sleep
import pygame
import os
import serial

# Get the current working directory and required files
current_directory = os.getcwd()
score_file_path = os.path.join(os.getcwd(), 'history/scores.txt')
player_car1_path = os.path.join(os.getcwd(), 'img/prado.png')
player_car2_path = os.path.join(os.getcwd(), 'img/Aston-Martin.png')
player_car3_path = os.path.join(os.getcwd(), 'img/rolls-royce.png')
player_car4_path = os.path.join(os.getcwd(), 'img/bugatti.png')
player_car5_path = os.path.join(os.getcwd(), 'img/rolls.png')
player_car6_path = os.path.join(os.getcwd(), 'img/keonig.png')
player_car7_path = os.path.join(os.getcwd(), 'img/benz1-fotor.png')
player_bike_path = os.path.join(os.getcwd(), 'img/bike-fotor.png')

enemy_car1_path = os.path.join(os.getcwd(), 'img/police-car2.png')
enemy_car2_path = os.path.join(os.getcwd(), 'img/police-car.png')
enemy_car3_path = os.path.join(os.getcwd(), 'img/lambo.png')
enemy_car4_path = os.path.join(os.getcwd(), 'img/pagani.png')

road_1_path = os.path.join(os.getcwd(), 'img/dark-yellow2-road.png')
road_2_path = os.path.join(os.getcwd(), 'img/dark-yellow2-road.png')

backGround_img_path = os.path.join(os.getcwd(), 'img/')
background_sound_path = os.path.join(os.getcwd(), 'sounds/gamemusic-6082.mp3')
crash_sound_path = os.path.join(os.getcwd(), 'sounds/mixkit-truck-crash-with-explosion-1616.wav')
new_level_sound_path = os.path.join(os.getcwd(), 'sounds/levelup.wav')
game_sound_start = os.path.join(os.getcwd(), 'sounds/futuristic-logo-3-versions-149429.mp3')

# Connect to Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)


def read_arduino_data():
    try:
        serial_data = arduino.readline().decode().strip().split(",")
        joystick_x = int(serial_data[0])
        joystick_y = int(serial_data[1])
        joystick_sw = int(serial_data[2])
        if not joystick_sw:
            joystick_sw = 0
    except (ValueError, IndexError):
        joystick_x, joystick_y = 0, 0

    if 0 <= joystick_x <= 250 and 251 <= joystick_y <= 558:
        return 1, joystick_sw
    elif 560 <= joystick_x and 402 <= joystick_y <= 558:
        return 2, joystick_sw
    elif 251 <= joystick_x <= 558 and 560 <= joystick_y:
        return 3, joystick_sw
    elif 251 <= joystick_x <= 558 and 0 <= joystick_y <= 250:
        return 4, joystick_sw
    return 0, joystick_sw


# function to read Scores on  the scores file
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


# function to save scores on a file
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


# function to scale the car images and return their dimensions

def scale_car(image_path, target_width=100):
    pygame.init()
    car_image = pygame.image.load(image_path)
    original_width, original_height = car_image.get_rect().size
    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio)

    scaled_car_image = pygame.transform.scale(car_image, (target_width, target_height))
    return scaled_car_image, target_width, target_height


increase_speed = (100, 200, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800,
                  5100, 5400, 5700, 6000, 6300, 6600, 6900, 7200, 7500, 7800, 8100)

levels = (1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000)


class CarRacing:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.display_width = 1200
        self.display_height = 900
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.crashed = False
        self.paused = False
        # Locating points
        self.m_right = int(self.display_width * (4 / 5) - 90)
        self.m_left = int(self.display_width * (1 / 5) + 40)
        self.count = 0
        self.h_scores, self.l_scores = read_scores()
        # player car
        self.player_car, self.scaled_car_width, car_height = scale_car(player_car2_path)
        self.car_x_coordinate = (self.display_width * 0.5)
        self.car_y_coordinate = (self.display_height * 0.7)
        # Background
        self.bg_img_height = self.display_height
        self.bg_img_width = int(self.display_width * 3 / 5)
        self.bgImg = pygame.image.load(road_1_path)
        self.bgImg = pygame.transform.scale(self.bgImg, (self.bg_img_width, self.bg_img_height))
        self.bg_speed = 3
        self.bg_x = int(self.display_width * (1 / 5))
        self.bg_y = 0
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
        self.game_menu_sound = pygame.mixer.Sound(game_sound_start)
        self.crash_sound = pygame.mixer.Sound(crash_sound_path)
        self.background_sound = pygame.mixer.Sound(background_sound_path)

        # initializing the screen
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        pygame.mixer.init()

    def menu(self):
        self.game_menu_sound.play()
        self.background_sound.stop()
        l_high_score, last_score = read_scores()
        menu_font = pygame.font.SysFont("comicsansms", 50)
        menu_loop = True
        while menu_loop:
            self.gameDisplay.fill((0, 0, 0))  # Fill the background with black
            menu_text = menu_font.render("Car Dodge", True, (255, 255, 255))
            self.gameDisplay.blit(menu_text, (self.display_width * 0.35, self.display_height * 0.2))
            play_text = menu_font.render("1. Play Game", True, (255, 255, 255))
            self.gameDisplay.blit(play_text, (self.display_width * 0.35, self.display_height * 0.4))
            quit_text = menu_font.render("2. Quit", True, (255, 0, 0))
            self.gameDisplay.blit(quit_text, (self.display_width * 0.35, self.display_height * 0.5))
            high_score_text = menu_font.render(f"High Scores = {l_high_score}", True, (100, 255, 100))
            last_score_text = menu_font.render(f"Last Scores = {last_score} ", True, (100, 100, 255))
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
                        self.game_menu_sound.stop()
                    elif event.key == pygame.K_2:
                        print("Goodbye!")
                        pygame.quit()
                        menu_loop = False

    def detect_collisions(self):

        if self.enemy_car_start_y <= self.car_y_coordinate <= (self.enemy_car_start_y + self.enemy_car_height - 30):
            if self.enemy_car_start_x <= self.car_x_coordinate <= (self.enemy_car_start_x + self.enemy_car_width) or \
                    self.enemy_car_start_x <= (self.car_x_coordinate + self.scaled_car_width) < (
                    self.enemy_car_start_x + self.enemy_car_width):
                self.crashed = True
                self.crash_sound.play()
                self.display_message("Game Over !!!")
        if self.car_x_coordinate < self.m_left or self.car_x_coordinate > self.m_right:
            self.crashed = True
            self.display_message("Game Over !!!")
        save_scores(self.count, self.count)

    def show_background(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y))
        self.gameDisplay.blit(self.bgImg, (self.bg_x, self.bg_y - self.display_height))

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.player_car, (car_x_coordinate, car_y_coordinate))

    def start_game(self):

        while True:
            self.__init__()
            self.menu()
            self.background_sound.play()
            while not self.crashed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.crashed = True
                        self.background_sound.stop()
                        save_scores(self.count, self.count)
                arduino_data, switch = read_arduino_data()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p]:
                    self.paused = True
                if keys[pygame.K_r]:
                    self.paused = False
                if self.paused:
                    self.display_message("Paused")
                    pygame.display.update()
                    continue
                if switch == 1:
                    self.change_vehicle()

                if arduino_data == 3:
                    self.car_x_coordinate -= 20  # Move left
                elif arduino_data == 4:
                    self.car_x_coordinate += 20  # Move right
                elif arduino_data == 1:
                    self.car_y_coordinate -= 20  # Move forward
                elif self.car_y_coordinate < (self.display_height * 0.78):
                    if arduino_data == 2:
                        self.car_y_coordinate += 20  # Move backward

                self.gameDisplay.fill((0, 0, 0))
                # Logic to loop road image
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
                self.highscore_and_speed()
                self.count += 1
                self.score_reward_vehicle()
                self.detect_collisions()
                pygame.display.update()
                self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 0, 0))
        self.gameDisplay.blit(text, (self.m_left, self.display_width * 1 / 3))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(2)

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def change_vehicle(self):
        if self.count < 2000 or self.count > 5000:
            if self.count > 6000 and self.count % 2 ==0:
                self.player_car, self.scaled_car_width, car_height = scale_car(player_car2_path)
            elif self.count % 3 == 0:
                self.player_car, self.scaled_car_width, car_height = scale_car(player_car1_path)
            elif self.count % 2 == 0:
                self.player_car, self.scaled_car_width, car_height = scale_car(player_car7_path)
            else:
                self.player_car, self.scaled_car_width, car_height = scale_car(player_bike_path)

    def score_reward_vehicle(self):
        if self.count > 5000:
            self.player_car, self.scaled_car_width, car_height = scale_car(player_car6_path)
            self.enemy_car, self.enemy_car_width, self.enemy_car_height = scale_car(enemy_car4_path)
        elif self.count > 4000:
            self.player_car, self.scaled_car_width, car_height = scale_car(player_car3_path)
            self.enemy_car, self.enemy_car_width, self.enemy_car_height = scale_car(enemy_car2_path)
        elif self.count > 3000:
            self.player_car, self.scaled_car_width, car_height = scale_car(player_car4_path)
            self.enemy_car, self.enemy_car_width, self.enemy_car_height = scale_car(enemy_car3_path)
        elif self.count > 2000:
            self.player_car, self.scaled_car_width, car_height = scale_car(player_car5_path)
            self.enemy_car, self.enemy_car_width, self.enemy_car_height = scale_car(enemy_car1_path)
        elif self.count > 1000:
            self.bg_speed = 6
            self.enemy_car_speed = 7.5

    def highscore_and_speed(self):
        font = pygame.font.SysFont("arial", 20)
        font2 = pygame.font.SysFont("lucidaconsole", 23)
        font3 = pygame.font.SysFont("arial", 11)
        font4 = pygame.font.SysFont("arial", 13)
        text = font.render("Scores : "+str(self.count), True, (100, 100, 0))
        text1 = font2.render("Your Records", True, (255, 255, 255))
        text2 = font.render(f"High Scores: {self.h_scores}", True, (160, 255, 160))
        text3 = font.render(f"Last Scores : {self.l_scores}", True, (160, 160, 255))
        text4 = font4.render(f"Hint : P  to pause", True, (100, 200, 200))
        text5 = font4.render(f"Hint : R to Resume ", True, (100, 200, 200))
        text6 = font3.render(f"To Every Level you get a reward ", True, (10, 100, 255))
        text7 = font3.render(f"a car reward  between Level 2 and 5 ", True, (10, 100, 255))
        text8 = font3.render(f"And  below or beyond those level ", True, (10, 100, 255))
        text9 = font3.render(f"you can  change a vehicle in 3 available", True, (10, 100, 255))
        text10 = font4.render(f"Hint : Click the JoyStick ", True, (100, 200, 255))
        self.gameDisplay.blit(text, (5, 0))
        self.gameDisplay.blit(text1, (5, 50))
        self.gameDisplay.blit(text2, (5, 100))
        self.gameDisplay.blit(text3, (5, 150))
        self.gameDisplay.blit(text4, (5, 200))
        self.gameDisplay.blit(text5, (5, 220))
        self.gameDisplay.blit(text6, (5, 520))
        self.gameDisplay.blit(text7, (5, 540))
        self.gameDisplay.blit(text8, (5, 560))
        self.gameDisplay.blit(text9, (5, 580))
        self.gameDisplay.blit(text10, (5, 600))
        speed_text = font.render(f"{int((self.count/100) +5)} MPH ", True, (0, 200, 200))
        menu_text = font.render(f"Level  {int(self.count/1000)} ", True, (0, 200, 200))
        self.gameDisplay.blit(menu_text, (10, 400))
        self.gameDisplay.blit(speed_text, (50, 450))
        if self.count in increase_speed:
            self.bg_speed += 1 + float(self.count / 1000.0)
            self.enemy_car_speed += 2 + float(self.count / 1000.0)
        if self.count in levels:
            pygame.mixer.Sound(new_level_sound_path).play()
        pygame.display.update()

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 18)
        text = font.render("Thanks for playing!", True, (255, 255, 255))
        self.gameDisplay.blit(text, (self.m_left, self.display_width * 2 / 3))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.start_game()
