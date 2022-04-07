import pygame
import subnets

pygame.init()

win = pygame.display.set_mode((800,400))
pygame.display.set_caption("Subnet Game")
clock = pygame.time.Clock()

INPUT_HOR = 350
INPUT_VER = 250
MENU = 0
GAME = 1
END = 2


back = pygame.image.load("sub11.jpg")

def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 30)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    return screen.blit(text_render, (x, y))

def redrawGameWindow(score, LIVES, color, input_rect, user_text):

    win.blit(back,(0,0))

    base_font = pygame.font.Font(None, 32)
    font = pygame.font.SysFont("comicsans", 30, True)
    # update question
    q_text = "Type in a subnet of 192.1.5.0/24"
    # q_text = "Give a subnet of " + subnets.generate()
    q_font = pygame.font.SysFont("comicsans", 30, True)
    question = q_font.render(q_text, 1 ,(0,0,0))
    win.blit(question, (150,150))

    # update score and life
    
    lives_text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(lives_text, (650,10))

    score_text = font.render("LIVES: " + str(LIVES), 1, (255,0,0))
    win.blit(score_text, (50,10))

    # user input area undate

    in_text = font.render("Your answer: ", 1, (0,0,255))
    win.blit(in_text, (INPUT_HOR - 200, INPUT_VER - 10))

    pygame.draw.rect(win, color, input_rect)
  
    text_surface = base_font.render(user_text, True, (255, 255, 255))
      
    # render at position stated in arguments
    win.blit(text_surface, (input_rect.x+5, input_rect.y+5))
      
    # set width of textfield
    input_rect.w = max(100, text_surface.get_width()+10)
      
    # update the screen
    pygame.display.flip()

    clock.tick(60)

def GAME():
    level = MENU
    # menu page setup
    while level == MENU:
        clock.tick(60)
        win.blit(back,(0,0))
        button_play = button(win, (350,250), "PLAY")
        button_quit = button(win, (350,300), "QUIT")
        menu_font = pygame.font.SysFont("comicsans", 50, True)
        menu_text = menu_font.render("Subnet Game " + "CLICK to PLAY", 1, (0,0,0))
        win.blit(menu_text, (50, 100))

        for event in pygame.event.get():
            # close the pygame when close window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    level = GAME
                if button_quit.collidepoint(event.pos):
                    pygame.quit()

        pygame.display.update()


    # user font
    user_text = ""

    #user input area
    input_rect = pygame.Rect(INPUT_HOR,INPUT_VER,140,32)

    # color when input box is clicked
    color_active = pygame.Color("blue")

    # color when input box is idle
    color_passive = pygame.Color('paleturquoise1')
    color = color_passive
    active = False




    score = 0
    LIVES = 3
    while level == GAME:

        pygame.time.delay(100)
        # button_menu = button(win, (750,350), "MENU")

        for event in pygame.event.get():
            # close the pygame when close window
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if button_menu.collidepoint(event.pos):
                #     level = MENU
                #     tomenu(level)
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # compare the answer

                    # change scores and clear answer
                    user_text = ""
                    if True:
                        score += 1
                        LIVES -= 1

                    # move to the next question

                else:
                    user_text += event.unicode

            if active:
                color = color_active
                        

            else: color = color_passive

            if LIVES == 0:
                level = END

        redrawGameWindow(score, LIVES, color, input_rect, user_text)

    while level == END:
        clock.tick(60)
        win.blit(back,(0,0))

        end_font = pygame.font.SysFont("comicsans", 50, True)
        end_text = menu_font.render("YOU LOSE", 1, (0,0,0))
        end_score = menu_font.render("YOUR SCORE IS " + str(score), 1, (0,0,0))
        win.blit(end_text, (100, 50))
        win.blit(end_score, (100, 150))
        button_re = button(win, (350,250), "RESTART")
        button_quit = button(win, (350,300), "QUIT")

        for event in pygame.event.get():
            # close the pygame when close window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_re.collidepoint(event.pos):
                    return True
                if button_quit.collidepoint(event.pos):
                    pygame.quit()

        pygame.display.update()

    return False
    
def main():
    playing = True
    while playing:
        playing = GAME()
    pygame.quit()
    
if __name__ == "__main__":
    main()

