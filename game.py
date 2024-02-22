import pygame
import time
import random

#To render font for time
pygame.font.init()

#Defining game window
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

player_width = 40
player_height = 50
player_speed = 5

rock_width = 10
rock_height = 20
rock_speed = 5

#Font and its size
font = pygame.font.SysFont("comicsans",20)
lost_font = pygame.font.SysFont("comicsans",60)

#Import background image
'''BG = pygame.transform.scale(pygame.image.load("moon.png"),(WIDTH, HEIGHT))[IF IAMGE IS SMALL]'''
BG = pygame.image.load("moon.png")


#Start draw
#display on game screen
def draw(player, elasped_time, rocks):
    #Background
    WIN.blit(BG, (0, 0))

    #Rendeer or display time
    time_text = font.render(f"Time: {round(elasped_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))


    #Display a rectangle.
    pygame.draw.rect(WIN, "red", player)

    #Drawing rocks after our palyer to appear on top
    for rock in rocks:
        pygame.draw.rect(WIN, "grey", rock)

    pygame.display.update()
#End draw


#Start main game function
def main():
    run = True

    #Draw Rectangle
    player = pygame.Rect(300, HEIGHT - player_height, player_width, player_height)

    #TO make player movement same in all computer.
    clock = pygame.time.Clock()

    #Track time
    start_time = time.time()
    elasped_time = 0

    #adding Rocks
    rock_add_increment  = 1000 #First rocks adds at 1000ms
    rock_count = 0 #Tells us when to add more rocks
    rocks = [] 
    hit = False 

    #Start loop
    while run:
        #Makes the loop work for 60 times in a sec.
        rock_count += clock.tick(60) #Tells us when to add more rocks to increase difficulty

        #Get time
        elasped_time = time.time() - start_time

        #Add rocks on screen. Runs after 2000ms to add more rocks.
        if rock_count > rock_add_increment:
            for _ in range(3): # adds 3 rocks.
                rock_x = random.randint(0, WIDTH - rock_width) #Random x position of rock
                rock = pygame.Rect(rock_x, -rock_height, rock_width, rock_height) #add rocks(rectangle) at x position a little heigher from screen
                rocks.append(rock) #add in our list

            #as more time passes the increment time of rocks decrease(more time = more rocks) 
            rock_dd_increment = max(200, rock_add_increment - 50) #cannot decrease less than 200ms and starts from 1000ms and gets -50 as time passes
            rock_count = 0 #restart the time to know when to add more rocks (increase the difficulty more)


        #Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        #Move left and right
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_speed >=0:#To limit the player in game screen
            player.x -= player_speed   
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and  player.x + player_speed + player_width <= WIDTH:#To limit the player in game screen
            player.x += player_speed             


        #Move rocks
        #Makes copy of the list to delete the rocks from it after it leaves the screen from bottom to save memory.
        #Loop through the copy list and upadte the og list
        for rock in rocks[:]: 
            rock.y += rock_speed #Increase the y axis so the rock moves from top to bottom
            if rock.y > HEIGHT: #If y axis is greater thaan height then enter.
                rocks.remove(rock)
            elif rock.y + rock.height>= player.y and rock.colliderect(player):
                rocks.remove(rock)
                hit = True
                break
        #When the rocks hits the rectangle
        if hit:
            lost = lost_font.render("You lost.",1 , "black")
            WIN.blit(lost,(WIDTH/2  - lost.get_width()/2, HEIGHT/2 - lost.get_height()/2)) #Get the lost text in centre of the screen
            pygame.display.update()
            pygame.time.delay(3000)
            break


        draw(player, elasped_time, rocks)
    #End loop

    pygame.quit()
#End Main
if __name__ == "__main__":
    main()
