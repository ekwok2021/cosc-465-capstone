
import pygame
from subnets import subnets


# ideas: Time -- scores
#        Complexity -- scores

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
MAXTIME = 100

base_font = pygame.font.Font(None, 32)
font = pygame.font.SysFont("comicsans", 30, True)
subnet_font = pygame.font.SysFont("comicsans", 25, True)
tip_font = pygame.font.SysFont("Ariel", 22, False)
result_font = pygame.font.SysFont("comicsans", 50, True)
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

def redrawGameWindow(score, LIVES, color_1, color_2, input_rect_1, input_rect_2, user_text_1, user_text_2, sub, timer_text):

    win.blit(back,(0,0))

    tip_font = pygame.font.SysFont("Ariel", 22, False)

    # update question
    q_text = "Give the range of subnet " + sub[1]
    question = font.render(q_text, 1 ,(0,0,0))
    win.blit(question, (WIDTH/2 - 350, HEIGHT / 2 -50))

    tip_text = tip_font.render("Press 'Enter' to submit", 1, (0,0,0))
    win.blit(tip_text, (WIDTH / 2 - 50, HEIGHT - 30))

    # put the timer 
    time = font.render("Time Left:", 1, (0,0,0))
    win.blit(time, (WIDTH / 2 - 100, 10))

    # update score and life
    lives_text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(lives_text, (WIDTH - 150,10))

    score_text = font.render("LIVES: " + str(LIVES), 1, (255,0,0))
    win.blit(score_text, (50,10))

    # user input area 1 update
    in_text_1 = font.render("Start range: ", 1, (0,0,255))
    win.blit(in_text_1, (INPUT_HOR - 200, INPUT_VER - 10))

    pygame.draw.rect(win, color_1, input_rect_1)
  
    text_surface_1 = base_font.render(user_text_1, True, (255, 255, 255))

    # user input area 2 update
    in_text_2 = font.render("End range: ", 1, (0,0,255))
    win.blit(in_text_2, (INPUT_HOR - 200, INPUT_VER + 40))

    pygame.draw.rect(win, color_2, input_rect_2)
  
    text_surface_2 = base_font.render(user_text_2, True, (255, 255, 255))

      
    # render at position stated in arguments
    win.blit(text_surface_1, (input_rect_1.x+5, input_rect_1.y+5))
    win.blit(text_surface_2, (input_rect_2.x+5, input_rect_2.y+5))
      
    # set width of textfield
    input_rect_1.w = max(100, text_surface_1.get_width()+10)
    input_rect_2.w = max(100, text_surface_2.get_width()+10)
      
    
    # timer
    win.blit(font.render(timer_text, True, (0,0,0)),(WIDTH/2 + 50, 10))

    # update the screen
    pygame.display.flip()

    clock.tick(60)

def resultGameWindow(timeout, correct, range1, range2):
    # change ranges from array to string

    str_r1 = ".".join(map(str,range1))

    str_r2 = ".".join(map(str,range2))

    while True:
        win.blit(back,(0,0))

        if correct:
            result_text = result_font.render("Your Answer is CORRECT", 1, (0,0,0))
            win.blit(result_text, (100, HEIGHT / 2 - 100))
        else: 
            if timeout:
                result_text = result_font.render("TIMEOUT!!", 1, (255,0,0))
            else:
                result_text = result_font.render("Your Answer is INCORRECT", 1, (0,0,0))
            win.blit(result_text, (50, HEIGHT / 2 - 100))
            answer_text = subnet_font.render("The correct range is " + str_r1 + " - " + str_r2, 1, (0,0,0))
            win.blit(answer_text, (50, HEIGHT / 2))
        tip_text = tip_font.render("Press Any key to continue", 1, (0,0,0))
        win.blit(tip_text, (WIDTH / 2 - 75, HEIGHT - 75))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return 10
        clock.tick(60)
        pygame.display.update()

# returns an array of 1) subnets in array form 2) subnets in string form
def generateSubnet():
    sub = subnets.genSubnet()
    last = str(sub[-1])
    s1 = sub[:-1]
    str_sub = ".".join(map(str,s1)) + "/" + last
    return [sub,str_sub]


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


     # color when input box is clicked
    color_active = pygame.Color("blue")

    # color when input box is idle
    color_passive = pygame.Color('paleturquoise1')

    user_text_1 = ""
    user_text_2 = ""
    #user input area
    input_rect_1 = pygame.Rect(INPUT_HOR,INPUT_VER,140,32)
    input_rect_2 = pygame.Rect(INPUT_HOR - 30,INPUT_VER + 50 ,140,32)

    color_1 = color_passive
    color_2 = color_passive
    active_1 = False
    active_2 = False
    score = 0
    LIVES = 3
    sub = generateSubnet()
    counter = MAXTIME
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    timer_text = str(counter).rjust(3)

    # --------------------------------------------------------

    while level == GAME:
        # initiate the correct answer and timeout
        timeout = False
        correct = False
        range1, range2 = subnets.addressRanges(sub[0])

        if counter <= 0:
            timeout = True
            resultGameWindow(timeout, correct, range1, range2)
            counter = MAXTIME
            timer_text = str(counter).rjust(3)
            sub = generateSubnet()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.USEREVENT:
                counter -= 1
                timer_text = str(counter).rjust(3)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_1.collidepoint(event.pos):
                    active_1 = True
                    active_2 = False
                else:
                    active_1 = False

                if input_rect_2.collidepoint(event.pos):
                    active_2 = True
                    active_1 = False
                else:
                    active_2 = False

            if event.type == pygame.KEYDOWN:
                if active_1:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_1 = user_text_1[:-1]
                    else: 
                        user_text_1 += event.unicode
                elif active_2:
                    if event.key == pygame.K_BACKSPACE:
                        user_text_2 = user_text_2[:-1]
                    else:
                        user_text_2 += event.unicode

                if event.key == pygame.K_RETURN:
                    range1, range2 = subnets.addressRanges(sub[0])
                    if timeout:
                        LIVES -= 1
                        resultGameWindow(timeout, correct, range1, range2)

                    # compare the answer

                    correct = subnets.compare(user_text_1, user_text_2, sub[1])

                    # change scores and clear answer
                    user_text_1 = ""
                    user_text_2 = ""
                    if correct and not timeout:
                        if counter >= 30:
                            score += 2
                        else:    
                            score += 1
                    else:
                        LIVES -= 1
                    
                    # display result window
                    resultGameWindow(timeout, correct, range1, range2)
                    counter = MAXTIME
                    timer_text = str(counter).rjust(3)
                    sub = generateSubnet()

            if active_1:
                color_1 = color_active
            else: color_1 = color_passive

            if active_2:
                color_2 = color_active
            else: color_2 = color_passive

            if LIVES == 0:
                level = END

        # win.blit(timer_font.render(timer_text, True, (0,0,0)), (32,48))
        # pygame.display.flip()
        redrawGameWindow(score, LIVES, color_1, color_2, input_rect_1, input_rect_2, user_text_1, user_text_2, sub, timer_text)

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

