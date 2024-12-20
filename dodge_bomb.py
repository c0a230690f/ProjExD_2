import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def game_over(screen: pg.Surface) -> None:
    go_bg = pg.Surface((1100,650))
    pg.draw.rect(go_bg,(0,0,0),[0,0,1100,650])
    go_bg.set_alpha(210)
    screen.blit(go_bg,[0,0])
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True,(255,255,255))
    go_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,0.9)
    screen.blit(go_img,[340,290])
    screen.blit(go_img,[720,290])
    screen.blit(txt,[400,300])
    pg.display.update()
    time.sleep(5)

# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     bb_img,bbaccs = init_bb_imgs()
#     avx = vx*bb_accs[min(tmr//500,9)]
#     bb_img = bb_imgs[min(tmr//500,9)]
#     accs = [a for a in range(1, 11)]
#     for r in range(1, 11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数であたえらrectが画面の中が外かを判定する
    引数:こうかとんrector 爆弾rect
    戻り値:真理値ダブル(横、縦)/画面内:Ture,画面外:False
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate
    # if kk_rct.colliderect(bb_rct):
    #    game_over(screen)

#改行いらないよ

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20)) #爆弾用にの空surface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) #爆弾円を描く
    bb_img.set_colorkey((0,0,0)) #
    bb_rct = bb_img.get_rect() #爆弾rectの抽出
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = 5,5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        # bb_img,bbaccs = init_bb_imgs()
        # avx = vx*bb_accs[min(tmr//500,9)]
        # bb_img = bb_imgs[min(tmr//500,9)]
        # accs = [a for a in range(1, 11)]
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            print("ゲームオーバー")
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら元の場所に戻す
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy) #爆弾動く
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
