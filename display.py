import pygame

pygame.init()

class Display:
    def __init__(self,res_w,res_h,title):
        self.w=res_w
        self.h=res_h
        self.title=title
        self.displaysurface=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption(self.title)

        while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()