from src.Game import *


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 60)
    game = Game()
    run = True
    while run:
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        game.WIN.blit(title_label, (game.WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.run_game()
                
    pygame.quit()


if __name__ == '__main__':
    # try:
        main_menu()
    # except Exception as e:
    #     print(f"There is an error occured: {e}")