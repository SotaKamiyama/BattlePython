import pygame
from pygame.locals import *
import sys, random
from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw()

# 変数の初期化
maze_w = 31# 迷路の列数
maze_h = 23# 迷路の行数
maze = []# 迷路データ
tile_w = 16
px = 1# プレイヤー x座標
py = 1# プレイヤー y座標
cx = 1# cpu x座標
cy = 1# cpu y座標

flg = 0# シーン用フラグ
minits = 0# タイム

# 背景画像ロード
pygame.init()
pygame.display.set_mode((tile_w*maze_w,tile_w*maze_h))
title = pygame.image.load("image/title.png").convert_alpha()

# 色を定義
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0,0,200)
green = (150,255,0)
white = (255,255,255)
brown = (100, 100, 90)
yellow = (250,100, 0)
maze_color = [black, blue, yellow]

# 迷路生成
def make_maze():
    global maze, px, py,cx,cy
    px = 1
    py = 1
    cx = 1
    cy = 1
    tbl = [[0,-1],[1,0],[0,1],[-1,0]]
    # 全部を0(通路)で初期化
    maze = []
    for y in range(0, maze_h):
        row = []
        for x in range(0, maze_w):
            row.append(0)
        maze.append(row)
    # 周囲を1(壁)で初期化
    for x in range(0, maze_w):
        maze[0][x] = 1
        maze[maze_h-1][x] = 1
    for y in range(0, maze_h):
        maze[y][0] = 1
        maze[y][maze_w-1] = 1
    # 棒倒し法で迷路を生成
    for y in range(2, maze_h-2):
        for x in range(2, maze_w-2):
            if x % 2 == 0 and y % 2 == 0:
                r = random.randint(0, 3)
                maze[y][x] = 1
                maze[y+tbl[r][1]][x+tbl[r][0]] = 1
    # ゴールを右下に設定
    maze[maze_h-2][maze_w-2] = 2

# 入力キーチェック
def check_key(key):
    global px, py,brown,flg
    old_x, old_y = px, py

    # playerの移動
    if key == K_LEFT:
        px -= 1
        
    elif key == K_RIGHT:
        px += 1
        
    elif key == K_UP:
        py -= 1
        
    elif key == K_DOWN:
        py += 1
    
    # 救済処置
    elif key == K_ESCAPE:
        pygame.quit()
        sys.exit()

    # シーン変移
    elif key == K_SPACE:
        flg += 1

        
    if maze[py][px] == 2 : # ゴール?
        if(flg == 1):
            messagebox.showinfo("ゴール","2階層へ")
            flg += 1
            main()
        if(flg == 2):
            messagebox.showinfo("ゴール","3階層へ")
            flg += 1
            main()
        if(flg == 3):# クリア
            messagebox.showinfo("ゴール","あなたの勝ち")
            flg += 1
            
                        
    if maze[py][px] != 0:
        px, py = old_x, old_y

def cpu():# cpu処理
    global cx,cy,flg
    old_cx, old_cy = cx, cy

    direc = random.randint(0,3)# 進行方向をランダムで選択

    if(direc == 0):
        cx -= 1
        pygame.time.wait(100)
    elif(direc == 1):
        cx += 1
        pygame.time.wait(100)
    elif(direc == 2):
        cy -= 1
        pygame.time.wait(100)
    elif(direc == 3):
        cy += 1
        pygame.time.wait(100)
    if maze[cy][cx] == 2 : # ゴール?
        messagebox.showinfo("ゴール","Pythonの勝ち")
        flg += 1
    if maze[cy][cx] != 0:
        cx, cy = old_cx, old_cy

    

def main():
    # ゲームの初期化処理   
    global px,py,cx,cy,flg
    pygame.init()
    pygame.display.set_caption("vs Python")
    screen = pygame.display.set_mode((tile_w*maze_w,tile_w*maze_h))
    rect = title.get_rect()

    # フォントロード
    font_title = pygame.font.Font(None, 50)
    font_press = pygame.font.Font(None, 25)
    

    # 描画文字列設定
    text_title = font_title.render("vs Python", True, (255,255,255))   
    text_press_space = font_press.render("Press Space", True, (255,255,255))
    text_press_escape = font_press.render("End", True, (255,255,255))
    text_press_re = font_press.render("Restart(press R)", True, (255,255,255))
    text_cong = font_title.render("Congratulations!!", True, (255,255,255))
    
    # 迷路作成
    make_maze()

    # ゲームのメインループ 
    while True:
        if(flg == 4):
            screen.fill(black)
            screen.blit(title,rect)
            screen.blit(text_cong,[80,80])
            screen.blit(text_press_escape, [100, 250])
            screen.blit(text_press_re, [250, 250])
            for event in pygame.event.get():
                if event.type == KEYDOWN: 
                    if event.key == K_r:# リスタート
                        flg = 0
                        main()  
                    check_key(event.key)# ESCキーで終了

        if(flg == 0):
            screen.fill(black)
            screen.blit(title,rect)
            screen.blit(text_title, [140, 100])
            screen.blit(text_press_space, [170, 200])
            
            for event in pygame.event.get():
                if event.type == KEYDOWN: 
                    check_key(event.key)
                

        if(flg == 1 or flg == 2 or flg == 3):
            # 迷路描画  
            for y in range(0, maze_h):
                for x in range(0, maze_w):
                    v = maze[y][x]
                    xx = tile_w * x
                    yy = tile_w * y
                    pygame.draw.rect(screen,
                            maze_color[v],
                            (xx,yy,xx+tile_w,yy+tile_w))
            # プレイヤーを円で描画する
            t2 = tile_w / 2
            pygame.draw.circle(screen, red,
                    (px * tile_w + t2, py * tile_w + t2), t2)
            
            # cpu playerと同じ座標に表示
            pygame.draw.circle(screen, green,
                    (cx * tile_w + t2, cy * tile_w + t2), t2)

            pygame.display.update()
            cpu()# cpu実行

        pygame.display.update()

        # イベント処理 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: 
                check_key(event.key)

if __name__ == '__main__':
    main()