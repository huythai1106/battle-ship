import pygame
from network import Network
from objects.button import Button
from until import *
pygame.font.init()

width = 700
height = 700

win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Client")


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))  # to mau nen background

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
            text = font.render("Your Move", 1, (0, 255, 255))
            win.blit(text, (50, 80))

            text = font.render("Opponents", 1, (0, 255, 255))
            win.blit(text, (400, 80))
        else:
            text = font.render("Opponents", 1, (0, 255, 255))
            win.blit(text, (50, 80))

            text = font.render("Your Move", 1, (0, 255, 255))
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
        if game.getStatusGame() == 2:
            turn = font.render("Turn : Your turn", 1, (255, 255, 255))

            if p == 0:
                if game.click == False:
                    turn = font.render("Turn : Your turn", 1, (255, 255, 255))
                else:
                    turn = font.render("Turn : Opponents' turn",
                                       1, (255, 255, 255))
            else:
                if game.click == True:
                    turn = font.render("Turn : Your turn", 1, (255, 255, 255))
                else:
                    turn = font.render("Turn : Opponents' turn",
                                       1, (255, 255, 255))

            win.blit(turn, (20, 20))

            for battle in game.maps:
                battle.draw(win)

    pygame.display.update()


# 3 nut bam
btns = Button("Submit", 250, 600, (255, 0, 255))


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            # lay du lieu game
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game1")
            break

        print(game.getStatusGame())

        # khi ca 2 player chon
        if game.bothWent():
            redrawWindow(win, game, player)
            # try:
            #     game = n.send("reset")
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
                                n.send("ready")
                            except pygame.error as e:
                                run = False
                                print(e)

            elif game.getStatusGame() == 2:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        n.send(make_pos(pos))

            # font = pygame.font.SysFont("comicsans", 90)
            # if (game.winner() == 0 and player == 0) or (game.winner() == 1 and player == 1):
            #     text = font.render("You won", 1, (255, 0, 0))
            # elif (game.winner() == -1):
            #     text = text = font.render("Tie game!", 1, (255, 0, 0))
            # else:
            #     text = font.render("You lost ...", 1, (255, 0, 0))
            # win.blit(text, (width / 2 - text.get_width() /
            #          2, height / 2 - text.get_height() / 2))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()


# main()
menu_screen()