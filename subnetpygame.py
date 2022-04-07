import pygame
import subnets

pygame.init()

WIDTH = 800
HEIGHT = 400

win = pygame.display.set_mode((WIDTH,HEIGHT))
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
    tip_font = pygame.font.SysFont("Ariel", 22, False)
    # update question
    q_text = "Type in a subnet of 192.1.5.0/24"
    # q_text = "Give a subnet of " + subnets.generate()
    q_font = pygame.font.SysFont("comicsans", 30, True)
    question = q_font.render(q_text, 1 ,(0,0,0))
    win.blit(question, (150,150))

    tip_text = tip_font.render("Press 'Enter' to submit", 1, (0,0,0))
    win.blit(tip_text, (WIDTH / 2 - 50, HEIGHT - 75))

    # update score and life
    
    lives_text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(lives_text, (WIDTH - 150,10))

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

def resultGameWindow(correct):
    while True:
        win.blit(back,(0,0))
        tip_font = pygame.font.SysFont("Ariel", 22, False)
        result_font = pygame.font.SysFont("comicsans", 50, True)
        if correct:
            result_text = result_font.render("Your Answer is CORRECT", 1, (0,0,0))
            win.blit(result_text, (100, HEIGHT / 2 - 100))
        else: 
            result_text = result_font.render("Your Answer is INCORRECT", 1, (0,0,0))
            win.blit(result_text, (50, HEIGHT / 2 - 100))
            answer_text = result_font.render("The correct range is " + "1-10", 1, (0,0,0))
            win.blit(answer_text, (50, HEIGHT / 2))
        tip_text = tip_font.render("Press Any key to continue", 1, (0,0,0))
        win.blit(tip_text, (WIDTH / 2 - 75, HEIGHT - 75))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return
        clock.tick(60)
        pygame.display.update()




def GAME():
    level = MENU
    # menu page setup
    while level == MENU:
        clock.tick(60)
        win.blit(back,(0,0))
        button_play = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 50), "PLAY")
        button_quit = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 100), "QUIT")
        menu_font = pygame.font.SysFont("comicsans", 50, True)
        menu_text = menu_font.render("Subnet Game " + "CLICK 'PLAY'", 1, (0,0,0))
        win.blit(menu_text, (50, HEIGHT / 2 - 100))

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # compare the answer
                    correct = False

                    # change scores and clear answer
                    user_text = ""
                    if correct:
                        score += 1
                        LIVES -= 1
                    else:
                        LIVES -= 1
                    
                    # display result window
                    resultGameWindow(correct)

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

        if score < 10:
            end_text = menu_font.render("YOU LOSE!", 1, (0,0,0))
        else: 
            end_text = menu_font.render("YOU WIN!!!", 1, (0,0,0))
        end_score = menu_font.render("YOUR SCORE IS " + str(score), 1, (255,0,0))
        win.blit(end_text, (100, 50))
        win.blit(end_score, (100, 150))
        button_re = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 50), "RESTART")
        button_quit = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 100), "QUIT")

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

