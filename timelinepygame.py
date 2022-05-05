
import pygame
import timeline

pygame.init()

WIDTH = 800
HEIGHT = 425

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Timeline Game")
clock = pygame.time.Clock()

INPUT_HOR = 350
INPUT_VER = 250
MENU = 0
GAME = 1
END = 2
MAXTIME = 10

base_font = pygame.font.Font(None, 32)
font = pygame.font.SysFont("comicsans", 30, True)
timeline_font = pygame.font.SysFont("Ariel", 30, True)
tip_font = pygame.font.SysFont("Ariel", 22, False)
result_font = pygame.font.SysFont("comicsans", 35, True)
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

def redrawGameWindow(score, LIVES, color_1, color_2, input_rect_1, input_rect_2, user_text_1, user_text_2, quest, timer_text):

    win.blit(back,(0,0))

    tip_font = pygame.font.SysFont("Ariel", 22, False)
    q_font = pygame.font.SysFont("Ariel", 36, False)
    bold_font = pygame.font.SysFont("Ariel", 36, True)

    # update question
    rtt = "round trip time: " + str(quest[0])
    bw = "bandwidth: " + str(quest[1])
    to = "timeout: " + str(quest[2])
    drop_seq = "sequence number of dropped packet: " + str(quest[3])

    text1 = "Given the info below, provide the                     and"
    text2 = "for the first data transmission after the drop:"
    q1 = q_font.render(text1, 1, (0,0,0))
    win.blit(q1, (WIDTH/2 - 350, HEIGHT/2 - 125))
    q2 = q_font.render(text2, 1, (0,0,0))
    win.blit(q2, (WIDTH/2 - 350, HEIGHT/2 - 100))
    st_text = bold_font.render("start time", 1, (0,0,0))
    win.blit(st_text, (WIDTH/2 + 50, HEIGHT/2 - 125))
    et_text = bold_font.render("end time", 1, (0,0,0))
    win.blit(et_text, (WIDTH/2 + 240, HEIGHT/2 - 125))

    margin = 75
    for info in [rtt, bw, to, drop_seq]:
        info_text = q_font.render(info, 1, (0,0,0))
        win.blit(info_text, (WIDTH/2 - 350, HEIGHT / 2 - margin))
        margin -= 25

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
    in_text_1 = font.render("Start time: ", 1, (0,0,150))
    win.blit(in_text_1, (INPUT_HOR - 200, INPUT_VER - 10))

    pygame.draw.rect(win, color_1, input_rect_1)
  
    text_surface_1 = base_font.render(user_text_1, True, (255, 255, 255))

    # user input area 2 update
    in_text_2 = font.render("End time: ", 1, (0,0,150))
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

def resultGameWindow(timeout, correct, answer):

    timeline.draw_graph(answer)
    graph = pygame.image.load("correct_timeline.jpg")
    w,h = graph.get_size()

    while True:
        win.blit(back,(0,0))
        win.blit(graph,(WIDTH - w,0))
        if correct:
            result_text = result_font.render("Your Answer is CORRECT", 1, (0,0,0))
            win.blit(result_text, (100, HEIGHT/2 - 100))
        else:
            if timeout:
                result_text = result_font.render("TIMEOUT!!", 1, (255,0,0))
            else:
                result_text = result_font.render("Your Answer is INCORRECT", 1, (0,0,0))
            win.blit(result_text, (50, HEIGHT/2 - 100))
        answer_text = timeline_font.render("The Correct Graph --->", 1, (0,0,0))
        win.blit(answer_text, (WIDTH/2 - 100, HEIGHT/2))
        tip_text = tip_font.render("Press Any key to continue", 1, (0,0,0))
        win.blit(tip_text, (WIDTH/2 - 175, HEIGHT - 75))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return True
        clock.tick(60)
        pygame.display.update()

# returns an array of 1) subnets in array form 2) subnets in string form
def generate_question():
    question = timeline.gen_question()
    answer = timeline.gen_answer_lines(question)
    return question, answer


def GAME():
    level = MENU
    # menu page setup
    while level == MENU:
        clock.tick(60)
        win.blit(back,(0,0))
        button_play = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 50), "PLAY")
        button_quit = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 100), "QUIT")
        menu_font = pygame.font.SysFont("comicsans", 50, True)
        menu_text = menu_font.render("Timeline Game " + "CLICK 'PLAY'", 1, (0,0,0))
        win.blit(menu_text, (50, HEIGHT / 2 - 100))

        for event in pygame.event.get():
            # close the pygame when close window
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    level = GAME
                if button_quit.collidepoint(event.pos):
                    pygame.quit()
                    return False

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
    question, answer = generate_question()
    counter = MAXTIME
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    timer_text = str(counter).rjust(3)

    # --------------------------------------------------------

    while level == GAME:
        # initiate the correct answer and timeout
        timeout = False
        correct = False

        if counter <= 0:
            timeout = True
            if not resultGameWindow(timeout, correct, answer):
                return False
            counter = MAXTIME
            timer_text = str(counter).rjust(3)
            LIVES -= 1
            if LIVES > 0: question, answer = generate_question()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
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
                    seq = 0
                    i = 0
                    j = 0
                    for l in answer:
                        if l.drop:
                            seq = l.seq
                            j = i + 1
                            break
                        i += 1
                    try:
                        start = int(user_text_1)
                        end = int(user_text_2)
                        line = timeline.Line("Data", start, end, seq, False)
                        answer_line = answer[j]
                        correct = (line == answer_line)
                    except ValueError:
                        correct = False

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
                    if not resultGameWindow(timeout, correct, answer):
                        return False
                    counter = MAXTIME
                    timer_text = str(counter).rjust(3)
                    if LIVES > 0 and score < 10: question, answer = generate_question()

            if active_1:
                color_1 = color_active
            else: color_1 = color_passive

            if active_2:
                color_2 = color_active
            else: color_2 = color_passive

            if LIVES == 0 or score >= 10:
                level = END

        redrawGameWindow(score, LIVES, color_1, color_2, input_rect_1, input_rect_2, user_text_1, user_text_2, question, timer_text)

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
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_re.collidepoint(event.pos):
                    return True
                if button_quit.collidepoint(event.pos):
                    pygame.quit()
                    return False

        pygame.display.update()

    return False
    
def main():
    playing = True
    while playing:
        playing = GAME()
    pygame.quit()
    
if __name__ == "__main__":
    main()

