import pygame
from network import Network
from objects.button import Button
from utils import *

pygame.font.init()
pygame.mixer.init()


width = 700
height = 700

win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Client")

base_font = pygame.font.Font(None, 32)
user_text: str = ''
text_box = pygame.Rect(100, 100, 140, 32)
color = pygame.Color('lightskyblue3')

background = pygame.image.load(
    "./assets/image/background.png").convert()

# pygame.mixer.music.load("./assets/audio/soundBG.mp3")
# pygame.mixer.music.set_volume(0.2)
net = Network()


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))  # to mau nen background
    win.blit(background, (0, 0))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width/2 - text.get_width() /
                 2, height/2 - text.get_height()/2))
    else:
        # print(game.maps)
        # p : player : stt nguoi choi
        font = pygame.font.SysFont("comicsans", 40)
        if p == 0:
            text = font.render("Your Move", 1, TEXT_COLOR)
            win.blit(text, (50, 80))

            text = font.render("Opponents", 1, TEXT_COLOR)
            win.blit(text, (400, 80))
        else:
            text = font.render("Opponents", 1, TEXT_COLOR)
            win.blit(text, (50, 80))

            text = font.render("Your Move", 1, TEXT_COLOR)
            win.blit(text, (400, 80))

        # prepare game
        if game.getStatusGame() == 1:
            font = pygame.font.SysFont("comicsans", 40)

            text1 = "Prepare..."
            text2 = "Prepare..."

            if game.p1Ready:
                text1 = "Lock In"
            if game.p2Ready:
                text2 = "Lock In"

            text1Render = font.render(text1, 1, (255, 0, 0, True))
            text2Render = font.render(text2, 1, (255, 0, 0, True))

            win.blit(text1Render, (50, 530))
            win.blit(text2Render, (400, 530))

            game.maps[p].draw(win)
            btns.draw(win)

        #  start game
        elif game.getStatusGame() == 2:
            turn = font.render("Turn : Your turn", 1, BLACK)

            if p == 0:
                if game.click == False:
                    turn = font.render("Turn : Your turn", 1, BLACK)
                else:
                    turn = font.render("Turn : Opponents' turn",
                                       1, BLACK)
            else:
                if game.click == True:
                    turn = font.render("Turn : Your turn", 1, BLACK)
                else:
                    turn = font.render("Turn : Opponents' turn",
                                       1, BLACK)

            win.blit(turn, (20, 20))

            for battle in game.maps:
                battle.draw(win)
                if battle.idMap == p:
                    for ship in battle.ships:
                        ship.draw(win)
                else:
                    for ship in battle.ships:
                        if ship.checkDead():
                            ship.draw(win)

    pygame.display.update()


# 3 nut bam
btns = Button("Submit", 250, 600, (255, 0, 255))

btnPlay = Button("Play", 100, 500, (255, 0, 255))


def main():
    run = True
    clock = pygame.time.Clock()

    if (user_text != ""):
        data = net.startConnect(user_text, 0)
        print(data)
    else:
        return

    try:
        player = int(net.getP())
        print("You are player", player)
    except:
        quit()

    while run:
        clock.tick(60)
        try:
            # lay du lieu game
            game = net.send("get")
        except:
            run = False
            print("Couldn't get game1")
            break

        # khi ca 2 player chon
        if game.bothWent():
            redrawWindow(win, game, player)

            # try:
            #     game = net.send("reset")
            # except:
            #     run = False
            #     print("Couldn't get game2")
            #     break

            if game.getStatusGame() == 1:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if btns.click(pos):
                            try:
                                net.send("submit")
                            except pygame.error as e:
                                run = False
                                print(e)
                        else:
                            net.send(make_pos(pos))
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN or event.key == pygame.K_w:
                            net.send("changeDirection")

            elif game.getStatusGame() == 2:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        net.send(make_pos(pos))
            elif game.getStatusGame() == 3:
                # try:
                #     game = net.send("reset")
                # except:
                #     run = False
                #     print("Couldn't get game2")
                #     break

                pygame.time.delay(500)
                font = pygame.font.SysFont("comicsans", 90)
                if (game.winner() == 0 and player == 0) or (game.winner() == 1 and player == 1):
                    text = font.render("You won", 1, (255, 0, 0))
                elif (game.winner() == -1):
                    text = font.render("Tie game!", 1, (255, 0, 0))
                else:
                    text = font.render("You lost ...", 1, (255, 0, 0))
                win.blit(text, (width / 2 - text.get_width() /
                         2, height / 2 - text.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(2000)

            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(win, game, player)


def menu_screen():
    global user_text

    run = True
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btnPlay.click(pos):
                    run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode.upper()

        win.fill((128, 128, 128))

        pygame.draw.rect(win, color, text_box, 2)

        text = base_font.render(user_text, 1, (255, 255, 0))
        win.blit(text, (text_box.x + 5, text_box.y + 5))

        text_box.w = max(100, text.get_width() + 10)
        btnPlay.draw(win)

        # font = pygame.font.SysFont("comicsans", 40)
        # text = font.render("Click to Play!", 1, (255, 0, 0))
        # win.blit(text, (100, 500))

        pygame.display.update()
        clock.tick(60)
    # pygame.mixer.music.play(-1)
    main()


# main()
menu_screen()
