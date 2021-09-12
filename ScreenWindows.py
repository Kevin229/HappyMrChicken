import random
from GifForPygame import GIFImage as GIFImage
import pygame.display
import Configuration as configApp
import time
from pygame import mixer

x_hen_list = []
y_hen_list = []
x_egg_list = []
y_egg_list = []
idx_chicken_list = []
icon_chicken_list = []
# List possible of x, y as windows and icon size
x_pos_choice = []
y_pos_choice = []
xy_choice_list = []

# Display gif when birth
idx_birth = 1


# jump as gravity
# return: current y value, true to start new cycle (1 up then 1 down), true to up jump
def jump_introduce_hen(distance_pixel, jump_second, start_time, current_time, up_jump):
    elapsed_time = current_time - start_time
    if up_jump:
        if elapsed_time > jump_second:
            y_hen = configApp.yPosHen - distance_pixel
            return y_hen, True, True
        else:
            y_hen = configApp.yPosHen
            v0_jump = int((distance_pixel + 9.8 * jump_second * jump_second / 2) / jump_second)
            delta_value = int(v0_jump * elapsed_time - 9.8 * elapsed_time * elapsed_time / 2)
            y_hen -= delta_value
            return y_hen, False, False
    else:
        if elapsed_time > jump_second:
            y_hen = configApp.yPosHen
            return y_hen, True, True
        else:
            y_hen = configApp.yPosHen - distance_pixel
            delta_value = int(distance_pixel * elapsed_time * elapsed_time / (jump_second * jump_second))
            y_hen += delta_value
            return y_hen, False, False


class ScreenWindows:
    def __init__(self,
                 icon_windows_path,
                 tittle_name,
                 screen_width,
                 screen_height):
        self.mIdx_birth = 1; #random.randrange(1, configApp.max_idx_chicken + 1)
        self.mIconPath = str(icon_windows_path)
        self.mTittleName = str(tittle_name)
        self.mScreenWidth = int(screen_width)
        self.mScreenHeight = int(screen_height)
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.mScreenWindows = pygame.display.set_mode((self.mScreenWidth, self.mScreenHeight))
        pygame.display.set_caption(str(tittle_name).upper())
        # windows_icon = pygame.image.load(str(icon_windows_path))
        # pygame.display.set_icon(windows_icon)
        self.mClock = pygame.time.Clock()
        self.mBRunning = False
        self.mPlaying = False
        self.mBirth = False
        self.mOutRange = False
        self.mIntroduceGif = GIFImage(configApp.introduceIconPath)
        self.mHenGif = GIFImage(configApp.henIconPath)
        self.mEggGif = GIFImage(configApp.eggIconPath)
        self.mIntroduceSound = pygame.mixer.Sound('sound/introduce.wav')
        self.mLayEggSound = pygame.mixer.Sound('sound/fartSound.wav')
        self.mEggCrackSound = pygame.mixer.Sound('sound/egg_crack.wav')
        self.mBirthSound = pygame.mixer.Sound('sound/chicken_dance.wav')

        # Build icon list GIFImage
        for i in range(configApp.max_idx_chicken):
            i += 1
            idx_icon_path = 'images/chicken_120pxl_width/chicken_' + str(i) + '.gif'
            icon_chicken_list.append(GIFImage(idx_icon_path))

    def draw_text(self,
                  msg,
                  x_pos,
                  y_pos,
                  width,
                  height,
                  text_color,
                  background_color,
                  is_button=False,
                  action=None):
        if not is_button:
            pygame.draw.rect(self.mScreenWindows,
                             text_color,
                             (x_pos, y_pos, width, height))
        else:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x_pos + width > mouse[0] > x_pos and y_pos + height > mouse[1] > y_pos:
                pygame.draw.rect(self.mScreenWindows,
                                 background_color,
                                 (x_pos, y_pos, width, height))
                if click[0] == 1 and None != action:
                    action()
            else:
                pygame.draw.rect(self.mScreenWindows,
                                 text_color,
                                 (int(x_pos), int(y_pos), int(width), int(height)))
        # smallText = pygame.font.SysFont("Courier", 50)
        smallText = pygame.font.Font('/Users/kevin/Library/Fonts/VNARABIA.TTF', 20)
        textSurface = smallText.render(msg, True, configApp.white_color)
        textRect = textSurface.get_rect()
        textRect.center = ((x_pos + (width / 2)), (y_pos + (height / 2)))
        self.mScreenWindows.blit(textSurface, textRect)
        pass

    def play_game(self):
        self.mPlaying = True
        self.mBirth = False
        pass

    def return_game(self):
        self.reset_game()
        self.mPlaying = False
        pass

    def reset_game(self):
        self.mBirth = False
        self.mOutRange = False
        self.mIdx_birth = random.randint(1, configApp.max_idx_chicken)
        # print(self.mIdx_birth)
        x_egg_list.clear()
        y_egg_list.clear()
        idx_chicken_list.clear()
        x_pos_choice.clear()
        y_pos_choice.clear()
        xy_choice_list.clear()
        if pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).stop()
        if pygame.mixer.Channel(3).get_busy():
            pygame.mixer.Channel(3).stop()
        pygame.mixer.Channel(0).play(self.mIntroduceSound, -1)

        # Create the x, y choice list
        row_num = random.randint(2, 8)
        col_num = random.randint(2, 9)
        space_row = configApp.chicken_icon + (configApp.screenHeight - configApp.num_row * configApp.chicken_icon) / (row_num + 1)
        space_col = configApp.chicken_icon + (configApp.screenWidth - configApp.num_col * configApp.chicken_icon) / (col_num + 1)
        x_pos = space_col - configApp.chicken_icon
        y_pos = space_row - configApp.chicken_icon
        while True:
            if x_pos < configApp.screenWidth:
                x_pos_choice.append(x_pos)
                x_pos += space_col
            else:
                break
        number_x = len(x_pos_choice)

        while True:
            if y_pos < configApp.screenHeight:
                y_pos_choice.append(y_pos)
                y_pos += space_row
            else:
                break
        number_y = len(y_pos_choice)
        for i in range(number_x):
            for j in range(number_y):
                xy = (x_pos_choice[i], y_pos_choice[j])
                xy_choice_list.append(xy)
        pass

    def quit_game(self):
        self.reset_game()
        quit()
        pass

    def crack_egg(self):
        self.mBirth = True
        self.mOutRange = False
        if pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).stop()
        if not pygame.mixer.Channel(2).get_busy():
            pygame.mixer.Channel(2).stop()
        if not pygame.mixer.Channel(3).get_busy():
            pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(2).play(self.mEggCrackSound)
        pygame.mixer.Channel(3).play(self.mBirthSound, -1)
        pass

    def buildWindows(self):
        self.mBRunning = True
        # start_time = time.time()
        # up_jump = True
        self.reset_game()
        while self.mBRunning:
            self.mClock.tick(60)
            self.mScreenWindows.fill(configApp.backGroundColor)
            # current_time = time.time()

            # Draw hen : introduce and list
            # y_hen_jump, jump_time, is_up = jump_introduce_hen(configApp.distance_pixel,
            #                                                   configApp.jump_seconds,
            #                                                   start_time,
            #                                                   current_time,
            #                                                   up_jump)
            # self.mScreenWindows.blit(self.mHenImg, (configApp.xPosHen, y_hen_jump))
            # self.mIntroduceGif.render(self.mScreenWindows,
            #                           (int(configApp.screenWidth/2 - self.mIntroduceGif.get_width()/2),
            #                            int(configApp.screenHeight/2 - self.mIntroduceGif.get_height()/2)))

            # # if finishing up or down, start new cycle
            # if jump_time:
            #     start_time = current_time
            # # if finishing, change up <-> down
            # if is_up:
            #     if up_jump:
            #         up_jump = False
            #     else:
            #         up_jump = True

            for i in range(len(x_hen_list)):
                self.mScreenWindows.blit(self.mHenImg, (x_hen_list[i], y_hen_list[i]))

            # Draw buttons
            if not self.mPlaying:
                self.mIntroduceGif.render(self.mScreenWindows,
                                          (int(configApp.screenWidth / 2 - self.mIntroduceGif.get_width() / 2),
                                           int(configApp.screenHeight / 2 - self.mIntroduceGif.get_height() / 2)))

                self.draw_text(configApp.tittleName,
                               int(configApp.screenWidth / 2 - 200),
                               100,
                               400,
                               100,
                               configApp.backGroundColor,
                               configApp.backGroundColor,
                               False,
                               action=None)

                self.draw_text('PLAY (1)',
                               int(configApp.screenWidth * 2 / 7),
                               600,
                               120,
                               50,
                               configApp.blue_color,
                               configApp.purple_color,
                               True,
                               action=self.play_game)

                # self.draw_text('RATE',
                #                int(configApp.screenWidth * 10 / 21),
                #                600,
                #                100,
                #                50,
                #                configApp.bright_green_color,
                #                configApp.purple_color,
                #                True,
                #                action=self.play_game)

                self.draw_text('QUIT (3)',
                               int(configApp.screenWidth * 14 / 21),
                               600,
                               120,
                               50,
                               configApp.blue_color,
                               configApp.purple_color,
                               True,
                               action=self.quit_game)
            else:
                for i in range(len(x_egg_list)):
                    x_pos_val = x_egg_list[i]
                    y_pos_val = y_egg_list[i]
                    if self.mBirth:
                        # icon_idx = idx_chicken_list[i]
                        icon_chicken_list[self.mIdx_birth].render(self.mScreenWindows,
                                                            (x_pos_val,
                                                             y_pos_val))
                    else:
                        self.mEggGif.render(self.mScreenWindows,
                                            (x_pos_val,
                                             y_pos_val))
                if not self.mBirth:
                    if len(x_egg_list):
                        self.mHenGif.render(self.mScreenWindows,
                                            (x_egg_list[len(x_egg_list) - 1] - 25,
                                             y_egg_list[len(x_egg_list) - 1] - 90))
                    else:
                        self.mHenGif.render(self.mScreenWindows,
                                            (int(configApp.screenWidth / 2 - self.mHenGif.get_width() / 2),
                                             int(configApp.screenHeight / 2 - self.mHenGif.get_height() / 2)))

                self.draw_text('CRACK (5)',
                               (configApp.screenWidth - 120) / 2,
                               20,
                               120,
                               50,
                               configApp.blue_color,
                               configApp.purple_color,
                               True,
                               action=self.crack_egg)

                self.draw_text('RESET (7)',
                               configApp.screenWidth - 140,
                               20,
                               120,
                               50,
                               configApp.blue_color,
                               configApp.purple_color,
                               True,
                               action=self.reset_game)

                self.draw_text('RETURN (9)',
                               configApp.screenWidth - 140,
                               90,
                               120,
                               50,
                               configApp.blue_color,
                               configApp.purple_color,
                               True,
                               action=self.return_game)

                self.draw_text(str(len(x_egg_list)),
                               20,
                               20,
                               100,
                               50,
                               configApp.blue_color,
                               configApp.purple_color,
                               False,
                               action=None)

                if self.mOutRange:
                    self.draw_text('OUT OF RANGE',
                                   (configApp.screenWidth - 300) / 2,
                                   (configApp.screenHeight - 50) / 2,
                                   300,
                                   50,
                                   configApp.blue_color,
                                   configApp.purple_color,
                                   False,
                                   action=None)

            for event in pygame.event.get():
                if self.mPlaying:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_7:
                            self.reset_game()
                        if event.key == pygame.K_9:
                            self.return_game()
                    if not self.mBirth:
                        if event.type == pygame.QUIT:
                            self.quit_game()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_5:
                                self.crack_egg()
                            else:
                                if self.mBirth:
                                    self.mBirth = False
                                if len(xy_choice_list):
                                    xy_i = random.choice(xy_choice_list)
                                    xy_choice_list.remove(xy_i)
                                    x_egg_list.append(xy_i[0])
                                    y_egg_list.append(xy_i[1])
                                    # idx_chicken_list.append(random.randint(0, configApp.max_idx_chicken - 1))
                                    if pygame.mixer.Channel(1).get_busy():
                                        pygame.mixer.Channel(1).stop()
                                    pygame.mixer.Channel(1).play(self.mLayEggSound)
                                else:
                                    self.mOutRange = True
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.play_game()
                        elif event.key == pygame.K_3:
                            self.quit_game()
                        else:
                            pass

            pygame.display.flip()
