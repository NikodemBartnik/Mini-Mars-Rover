import pygame, math, time, socket
import gui

s = socket.socket()  
pygame.init()

screen = pygame.display.set_mode([800, 800])
mousePressed = False

s.bind(('', 12345))  
s.listen(5)
c, addr = s.accept()

def sendToRobot(c):
    c.send((str(round(slider1.getValue()*1800)) + "," + str(round(slider2.getValue()*1800)) + "," + str(round(slider3.getValue()*1800)) + "," + str(round(slider4.getValue()*1800)) + "," + str(round(joystick.getValue()[0]*10)) + "," + str(round(joystick.getValue()[1]*100)) + "," + str(1 if camera_button.getValue() == True else 0) + "," + str(1 if turn_left_button.getValue() == True else 2 if turn_right_button.getValue() else 0) + '\n').encode())
    #print(c.recv(10))

def clickCheck(pos, clicked):
    slider2.checkIfPressed(pos, clicked)
    slider1.checkIfPressed(pos, clicked)
    slider3.checkIfPressed(pos, clicked)
    slider4.checkIfPressed(pos, clicked)
    joystick.checkIfPressed(pos, clicked)
    camera_button.checkIfPressed(pos, clicked)
    turn_left_button.checkIfPressed(pos, clicked)
    turn_right_button.checkIfPressed(pos, clicked)

def drawAll():
    slider1.draw(screen)
    slider2.draw(screen)
    slider3.draw(screen)
    slider4.draw(screen)
    title1.draw(screen)
    title2.draw(screen)
    title3.draw(screen)
    title4.draw(screen)
    title5.draw(screen)
    joystick.draw(screen)
    title6.draw(screen)
    camera_button.draw(screen)
    turn_left_button.draw(screen)
    turn_right_button.draw(screen)
    title7.draw(screen)
    titleL.draw(screen)
    titleR.draw(screen)


slider1 = gui.Slider((170,50), 500, 0.5)
slider2 = gui.Slider((170,120), 500, 0.5)
slider3 = gui.Slider((170,190), 500, 0.5)
slider4 = gui.Slider((170,260), 500, 0.5)
title1 = gui.Title((60, 45), "Servo 1")
title2 = gui.Title((60, 115), "Servo 2")
title3 = gui.Title((60, 185), "Servo 3")
title4 = gui.Title((60, 255), "Jaw")
title5 = gui.Title((200,360), "Robot control")
joystick = gui.Joystick((260,550), 120)
title6 = gui.Title((575,360), "Camera")
camera_button = gui.Button((610, 450), 30)
title7 = gui.Title((590,560), "Turn")
titleL = gui.Title((545,620), "L")
titleR = gui.Title((675,620), "R")
turn_left_button = gui.Button((550, 630), 30, False, False)
turn_right_button = gui.Button((680, 630), 30, False, False)




while 1:
    screen.fill((40,40,40))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False
        if event.type == pygame.QUIT:
            pygame.quit()
        clickCheck(pygame.mouse.get_pos(), mousePressed)
        
    sendToRobot(c)
    print(turn_left_button.getValue())
    drawAll()

    time.sleep(0.01)
    pygame.display.flip()
