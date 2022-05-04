from asyncio.windows_events import NULL
import pygame
import routing
from routing import Gengraphs
from simulator import AutonomousSystem
import math
import numpy as np

# Traffic cannot traverse a 
# provider-customer link followed by a customer-provider or peering link
#  — implies customer is providing transit for providers or peers



pygame.init()

WIDTH = 800
HEIGHT = 400
PIC_SIZE = 38

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Routing Game")
clock = pygame.time.Clock()

LOCATION_LIST = [(100, 50), (200, 100), (100, 200), (300, 300), (300, 150), (500, 50), (600, 250)]
LOCATIONS = {}
HITBOX = {}

MENU = 0
EASY = 1
MEDIUM = 2
HARD = 3
TUTORIAL = False

WIN = 99
LOSE = 18

IDLE = pygame.image.load("AS.png")
ACTIVATE = pygame.image.load("AS_Activate.png")
END = pygame.image.load("AS_end.png")

base_font = pygame.font.Font(None, 32)
font = pygame.font.SysFont("comicsans", 30, True)
tt_font = pygame.font.SysFont("comicsans", 18, True)
as_font = pygame.font.SysFont("Ariel", 15, False)
result_font = pygame.font.SysFont("comicsans", 50, True)
back = pygame.image.load("back.jpg")
blank = pygame.image.load("blank.jpg")

def button(screen, position, text, size):
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    return screen.blit(text_render, (x, y))
      
def Createhitbox(ver, hor):
    hit = pygame.Rect(ver,hor,38,38)
    return hit

def ChangeLoc(direction, pos1_hor, pos1_ver, pos2_hor, pos2_ver):

    # 0 = right-up, 1 = left-up, 2 = right-down, 3 = left-down
    if direction % 2 == 0:
        pos1_hor += PIC_SIZE
    else:
        pos2_hor += PIC_SIZE
    if direction > 1:
        pos1_ver += PIC_SIZE
    else:
        pos2_ver += PIC_SIZE
    return ((pos1_hor, pos1_ver), (pos2_hor, pos2_ver))

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    direction = 0
    # decide where the arrow points to

    if x1 > x2: # point to left
        direction += 1
    if y1 < y2: # point down
        direction += 2

    p1, p2 = ChangeLoc(direction, x1, y1, x2, y2)
    x1, y1 = p1
    x2, y2 = p2

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in np.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in np.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)
    pygame.display.flip()

def Drawarrow(pos1_hor, pos1_ver, pos2_hor, pos2_ver):
    direction = 0
    # decide where the arrow points to

    if pos1_hor > pos2_hor: # point to left
        direction += 1
    if pos1_ver < pos2_ver: # point down
        direction += 2

    pos1, pos2 = ChangeLoc(direction, pos1_hor, pos1_ver, pos2_hor, pos2_ver)


    pygame.draw.line(win, (0,0,0), (pos1[0], pos1[1]), (pos2[0], pos2[1]))

    arrow=pygame.Surface((50,50))
    arrow.fill((255,255,255))
    pygame.draw.line(arrow, (0,0,0), (0,0), (25,25))
    pygame.draw.line(arrow, (0,0,0), (0,50), (25,25))
    arrow.set_colorkey((255,255,255))

    angle=math.atan2(-(pos1[1] -pos2[1]), pos1[0] - pos2[0] )
    angle=math.degrees(angle)

    def drawAng(angle, pos):
        nar=pygame.transform.rotate(arrow,angle)
        nrect=nar.get_rect(center=pos)
        win.blit(nar, nrect)

    # drawAng(angle, pos1)
    angle+=180
    drawAng(angle, (pos2[0], pos2[1]))
    pygame.display.flip()

def redrawGameWindow(activated, idled, end, ases, step):
        win.blit(blank,(0,0))
        button(win, (WIDTH- 100, HEIGHT / 2 + 120), "TUTORIAL", 20)
        step_text = font.render("Step: "+ str(step), 1, (0,0,0))
        win.blit(step_text, (WIDTH/2 - 100, 20))
        button(win, (WIDTH- 100, HEIGHT / 2 + 150), "RESTART", 20)
        button(win, (WIDTH - 100, HEIGHT / 4 - 90), "MENU", 30)

        for a in activated:
            as_text = as_font.render("AS " + str(a) , 1 , (0,0,0))
            win.blit(ACTIVATE, (LOCATIONS[a][0], LOCATIONS[a][1]))
            win.blit(as_text, (LOCATIONS[a][0], LOCATIONS[a][1] + PIC_SIZE + 3))
        for i in idled:
            as_text = as_font.render("AS " + str(i) , 1 , (0,0,0))
            win.blit(IDLE, (LOCATIONS[i][0], LOCATIONS[i][1]))
            win.blit(as_text, (LOCATIONS[i][0], LOCATIONS[i][1] + PIC_SIZE + 3))

        win.blit(END, (LOCATIONS[end][0], LOCATIONS[end][1]))

        already = []
        for AS in ases:
            # only create arrows to providers for now
            providers = ases[AS]["providers"]
            peers = ases[AS]["peers"]
            AS_pos = LOCATIONS[AS]
            for pro in providers:
                Drawarrow(AS_pos[0], AS_pos[1], LOCATIONS[pro][0], LOCATIONS[pro][1])
            for peer in peers:
                if peer not in already:
                    draw_dashed_line(win, "blue", AS_pos, LOCATIONS[peer])
                    already.append(AS)

        pygame.display.update()


        

def GAME(level):
    menu_font = pygame.font.SysFont("comicsans", 50, True)
    # menu page setup
    while level == MENU:
        clock.tick(60)
        win.blit(back,(0,0))
        button_play = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 50), "PLAY", 30)
        button_quit = button(win, (WIDTH / 2 - 50, HEIGHT / 2 + 100), "QUIT", 30)
        menu_text = menu_font.render("Routing Game ", 1, (0,0,0))
        win.blit(menu_text, (WIDTH/2 -150, HEIGHT / 2 - 100))

        for event in pygame.event.get():
            # close the pygame when close window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    level = EASY
                if button_quit.collidepoint(event.pos):
                    pygame.quit()

        pygame.display.update()
    
# -----------------------------------------------------------------------------------
    ases = routing.Gengraphs(level) # dict
    start, end = routing.Genroute(ases) # int
    restart = True
    TUTORIAL = False

    def init_game():
        # Initialize the graph
        activated = []
        idled = []
        count = 0
        #print(ases)
        for n in ases.keys():
            LOCATIONS.update({n: LOCATION_LIST[count]})
            if n == start:
                activated.append(n)
            else:
                idled.append(n)
            count += 1
        #print(LOCATIONS)
        return activated, idled

    def tutorial_page():
        win.blit(blank,(0,0))
        clock.tick(5)
        # Explanation for icons
        idle_text = tt_font.render("AS, click it to activate.(think about AS relationships before you click!)", 1 , (0,0,0))
        win.blit(IDLE, (50, 50))
        win.blit(idle_text, (100, 50))

        act_text = tt_font.render("Activated AS, you can only move to ASes next to the last activated.", 1 , (0,0,0))
        win.blit(ACTIVATE, (50, 100))
        win.blit(act_text, (100, 100))
        
        end_text = tt_font.render("Destination AS, try to get there without violating the Valley-free rule", 1 , (0,0,0))
        win.blit(END, (50, 150))
        win.blit(end_text, (100, 150))

        Drawarrow(12, 192, 100, 230)
        arrow_text = tt_font.render("Arrow represents FROM customer TO provider relationship", 1 , (0,0,0))
        win.blit(arrow_text, (130, 220))

        draw_dashed_line(win, "blue", (12, 242), (102, 280))
        dash_text = tt_font.render("Dashed lines represents peer relationships", 1 , (0,0,0))
        win.blit(dash_text, (130, 280))


        while True:
            button_back = button(win, (WIDTH- 100, HEIGHT / 2 + 120), "back", 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_back.collidepoint(event.pos):
                            return False
            pygame.display.update()

    def result_page(outcome, level):
          while True:
            win.blit(blank,(0,0))
            button_menu = button(win, (WIDTH / 2 - 100 , HEIGHT / 2 + 130), "MENU", 30)
            button_re = button(win, (WIDTH / 2 - 100, HEIGHT / 2 + 70), "TRY AGAIN", 30)

            if outcome == LOSE:
                result_text = menu_font.render("YOU LOSE!", 1, (0,0,0))
                t_text = tt_font.render("Hint: Traffic cannot traverse a provider-customer ", 1, (0,0,0)) 
                t1_text = tt_font.render("link followed by a customer-provider or peering link ", 1, (0,0,0))
                win.blit(t_text, (150, HEIGHT/2 - 20))
                win.blit(t1_text, (150, HEIGHT/2 + 10))
            else:
                result_text = menu_font.render("YOU WIN!", 1, (255,0,0))
                button_next = button(win, (WIDTH / 2 - 100, HEIGHT / 2 + 10), "NEXT LEVEL", 30)
            win.blit(result_text, (250, HEIGHT / 2 - 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_re.collidepoint(event.pos):
                        return level
                    if outcome == WIN and button_next.collidepoint(event.pos):
                        return level + 1
                    if button_menu.collidepoint(event.pos):
                        return MENU
                    
                pygame.display.update()

            



# Traffic cannot traverse a 
# provider-customer link followed by a customer-provider or peering link
#  — implies customer is providing transit for providers or peers

    pre = NULL
    pre_cus = False
    current = start
    step = 0
    while True:
        clock.tick(10)
        if restart:
            activated, idled = init_game()
            restart = False
            pre = NULL
            pre_cus = False
            current = start
            step = 0
        
        ttl_input = pygame.Rect(WIDTH- 100, HEIGHT / 2 + 120, 90, 20)
        rs_input = pygame.Rect(WIDTH- 100, HEIGHT / 2 + 150, 80, 20)
        menu_input = pygame.Rect(WIDTH- 100, HEIGHT / 4 - 90, 80, 30)
        
        #print(ases)

        # create hitbox for each AS icon
        for key in LOCATIONS:
            x,y = LOCATIONS[key]
            hitbox = Createhitbox(x,y)
            HITBOX.update({key: hitbox})


        for event in pygame.event.get():
            # close the pygame when close window
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ttl_input.collidepoint(event.pos):
                    TUTORIAL = tutorial_page()
                elif rs_input.collidepoint(event.pos):
                    restart = True
                elif menu_input.collidepoint(event.pos):
                    return MENU

                cur_dict = ases[current]
                # check all routers and change their states
                for k in HITBOX:
                    icon = HITBOX[k]
                    activate = False
                    cancel = False
                    if icon.collidepoint(event.pos):

                        # decide the AS's relationship with the current one
                        if k in cur_dict["customers"]:
                            if k not in activated:
                                pre_cus = True
                                activate = True
                        elif k in cur_dict["peers"] or k in cur_dict["providers"]:
                            if not pre_cus:
                                activate = True
                            else:
                                return (result_page(LOSE, level))
                        elif k == current:
                            cancel = True
                        if activate:
                            pre = current
                            current = k
                            activated.append(k)
                            idled.remove(k)
                            step += 1
                        if cancel and pre != NULL:
                            current = pre
                            activated.remove(k)
                            idled.append(k)
                            step += 1
                if current == end:
                    return (result_page(WIN, level))


        #print(activated)
        if not TUTORIAL:
            redrawGameWindow(activated, idled, end, ases, step)
    


def main():
    playing = True
    level = 0
    while playing:
        result = GAME(level)
        level = result
    pygame.quit()
    
if __name__ == "__main__":
    main()