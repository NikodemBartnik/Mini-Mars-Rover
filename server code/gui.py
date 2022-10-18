from re import S
import pygame, math


class Slider:
    def __init__(self, pos, length, default=0) -> None:
        self.pos = pos
        self.length = length
        self.height = 15
        self.colorBackground = (80,80,80)
        self.colorDot = (230,230,230)
        self.dotPos = (self.pos[0] + self.length * default, self.pos[1]+7)
        self.value_display = Title((self.pos[0]+self.length+20, self.pos[1]-5), str(self.getValue()))


    def checkIfPressed(self, click_pos, clicked):
        if(clicked and self.pos[0] < click_pos[0] and (self.pos[0] + self.length) > click_pos[0] and
        self.pos[1] < click_pos[1]  and (self.pos[1] + self.height*2.5) > click_pos[1]):
            self.dotPos = (click_pos[0], self.dotPos[1])
            self.value_display.change(str(self.getValue()))
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.colorBackground, (self.pos[0], self.pos[1], self.length, self.height))
        pygame.draw.circle(screen, self.colorDot, self.dotPos, 15)
        self.value_display.draw(screen)
    
    def getValue(self):
        return (self.dotPos[0] - self.pos[0])/self.length

    def setValue(self, val):
        self.dotPos = (self.pos[0] + (self.length * val), self.pos[1])


class Title:
    def __init__(self, pos, title) -> None:
        self.pos = pos
        self.title = title
        self.font = pygame.font.SysFont('arial', 20)
        self.text = self.font.render(self.title, False, (100, 100, 100))

    def change(self, title):
        self.text = self.font.render(title, False, (100, 100, 100))

    def draw(self, screen):
        screen.blit(self.text, self.pos)


class Joystick:
    def __init__(self, pos, size) -> None:
        self.pos = pos
        self.size = size
        self.colorBackground = (80,80,80)
        self.colorDot = (230,230,230)
        self.JOYSTICKLIMIT = size
        self.clicked = False

    def checkIfPressed(self, click_pos, clicked):
    
        if (clicked and (click_pos[0] - self.pos[0]) ** 2 + (click_pos[1] - self.pos[1]) ** 2 < (self.size ** 2)):
            self.clicked = True
            return True
        else:
            self.clicked = False
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.colorBackground, self.pos, self.size)
        if(self.clicked):
            pygame.draw.circle(screen, self.colorDot, self.limitJoystickMovment(self.pos, pygame.mouse.get_pos()), self.size*0.6)

    def limitJoystickMovment(self, pos1, pos2):
        if pos1[0] > pos2[0]:
            x = pos1[0] - self.JOYSTICKLIMIT if pos1[0] - pos2[0] > self.JOYSTICKLIMIT else pos2[0]
        else:
            x = pos1[0] + self.JOYSTICKLIMIT if pos2[0] - pos1[0] > self.JOYSTICKLIMIT else pos2[0]
        if pos1[1] > pos2[1]:
            y = pos1[1] - self.JOYSTICKLIMIT if pos1[1] - pos2[1] > self.JOYSTICKLIMIT else pos2[1]
        else:
            y = pos1[1] + self.JOYSTICKLIMIT if pos2[1] - pos1[1] > self.JOYSTICKLIMIT else pos2[1]
        return (x, y)

    def getValue(self):
        if self.clicked:
            return [(math.atan2(pygame.mouse.get_pos()[1] - self.pos[1], pygame.mouse.get_pos()[0] - self.pos[0]) * 180/math.pi) + 180, math.sqrt((self.pos[0]-pygame.mouse.get_pos()[0])**2+(self.pos[1]-pygame.mouse.get_pos()[1])**2)/self.size]
        else:
            return -1, 0


class Button:
    def __init__(self, pos, size, clicked = False, bistable = True) -> None:
        self.pos = pos
        self.size = size
        self.colorBackground = (80,80,80)
        self.colorDot = (230,230,230)
        self.clicked = clicked
        self.bistable = bistable

    def draw(self, screen):
        pygame.draw.circle(screen, self.colorBackground, self.pos, self.size)
        if(self.clicked):
            pygame.draw.circle(screen, self.colorDot, self.pos, self.size*0.6)

    def checkIfPressed(self, click_pos, clicked):
    
        if (clicked and self.clickFlag is False and (click_pos[0] - self.pos[0]) ** 2 + (click_pos[1] - self.pos[1]) ** 2 < (self.size ** 2)):
            self.clickFlag = True
            if self.bistable:
                self.clicked = not self.clicked
            else:
                self.clicked = True
        else:
            self.clickFlag = False
            if not self.bistable:
                self.clicked = False
            return False

    def getValue(self):
        return self.clicked