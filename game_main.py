""" justwindow. py """
# -*- coding: utf-8 -*-
import pygame
import cards
import sys
import re
from pygame.locals import *
from mutagen.mp3 import MP3 as mp3
import time

pygame.init()
pygame.display.set_caption("cool 104")

bgm_file = 'ipa.mp3'

fontsize = 36                                         # フォントサイズ
fontcolor = [200,200,0]                               # フォントの色
sysfont = pygame.font.Font("ipag.ttf", fontsize)

# 画面
SURFACE = pygame.display.set_mode((1034, 900))  # 全体画面の大きさ

surfacecolor = [0,0,100]                        # 背景色
line_c = (255,0,0)                              # 選択可能なカードの枠
FPSCLOCK = pygame.time.Clock()                  # 画面の描画

img_dir = "card_image/"           # カードのファイルディレクトリ
cards_list = [""] * 52            # 全カードリスト
cards_str = [""] * 6              # 個別カードの文字
cards_file = [""] * 6             # 個別カードのファイル名
cards_image = [""] * 6            # 個別カードのイメージファイルパス
cards_index = [0, 1, 2, 3, 4, 5]  # カードのインデックス
cards_ok = [0,1,1,1,1,1]          # カードが選択可能か（第一引数のセンターカードは必ず"0"）

orbit = 1                         # 周回（何週目か。初期化前は"0"）

comment = ""                      # コメント

# カードの大きさ、配置場所
scale = 0.25                           # 1/4スケール
card_width_org = 712                   # original size
card_height_org = 1008                 # original size
card_width = card_width_org * scale    # 178
card_height = card_height_org * scale  # 252
disp_card_spa = 24                     # 手札カードの間隔
disp_card_s_y = 100                    # センターカードのy座標
disp_card_y = 500                      # 手札カードのy座標


# カードの配置場所(rect)
cards_xy = [] * 6
cards_xy.append(pygame.Rect(disp_card_spa * 3 + card_width * 2, disp_card_s_y,card_width,card_height))  # センターカード
cards_xy.append(pygame.Rect(disp_card_spa, disp_card_y,card_width,card_height))                         # 左から１番目
cards_xy.append(pygame.Rect(disp_card_spa * 2 + card_width * 1, disp_card_y, card_width, card_height))  # 左から２番目
cards_xy.append(pygame.Rect(disp_card_spa * 3 + card_width * 2, disp_card_y, card_width, card_height))  # 左から３番目
cards_xy.append(pygame.Rect(disp_card_spa * 4 + card_width * 3, disp_card_y, card_width, card_height))  # 左から４番目
cards_xy.append(pygame.Rect(disp_card_spa * 5 + card_width * 4, disp_card_y, card_width, card_height))  # 左から５番目

# 使用カードリスト作成

pay_c_fontsize = 100                                           # フォントサイズ
pay_c_font = pygame.font.Font("ipag.ttf", pay_c_fontsize)     # フォント
pay_c_fontcolor_y = [255,255,0]                               # フォントの色：黄色
pay_c_fontcolor_w = [255,255,255]                             # フォントの色：白
pay_c_fontcolor_b = [0,0,0]                                   # フォントの色：黒


pay_c_col = [] * 13
pay_c_y = 150    # 使用カード表示のy座標
pay_c_x = 630    # 使用カード表示のx座標
pay_c_spa = 25
pay_c_buf = pay_c_spa * 2
pay_c_line = 50
pay_c_list = [] * 52

# カウントの表示場所（380,100+252-36）
count_xy = pygame.Rect(card_width * 2 - pay_c_spa * 4 ,disp_card_s_y + card_height - pay_c_fontsize , card_width , card_height)
count_fra_xy = pygame.Rect(card_width * 2 - pay_c_spa * 4 ,disp_card_s_y + card_height - pay_c_fontsize ,pay_c_fontsize * 1.6,pay_c_fontsize)


# マーク部位表示
pay_back_xy = pygame.Rect([disp_card_spa * 4 + card_width * 3,pay_c_y,pay_c_spa * 15,pay_c_line * 4-10]) # 使用カード枠
pay_Mark_s = pygame.transform.rotozoom(pygame.image.load(img_dir + "s.png"), 0, scale * 0.8)
pay_Mark_h = pygame.transform.rotozoom(pygame.image.load(img_dir + "h.png"), 0, scale * 0.8)
pay_Mark_c = pygame.transform.rotozoom(pygame.image.load(img_dir + "c.png"), 0, scale * 0.8)
pay_Mark_d = pygame.transform.rotozoom(pygame.image.load(img_dir + "d.png"), 0, scale * 0.8)


def main():
    """ main routine """
    global cards_image
    global cards_xy
    global cards_count
    global cards_str
    global cards_file
    global cards_image
    global cards_list
    global orbit
    global message
    cards_count = 1   # カードのカウント数

    pygame.mixer.music.load(bgm_file)
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)
    while True:
        # リストが空で手札がないときリストを作成する
        if all([x == "" for x in cards_list]) and all([x == "" for x in cards_str[1:]]):
            cards_list = cards.payout_list(cards_str[0],1)

        # 手札カードがなくなったらリストから補充する
        for i,v in enumerate(cards_str):
            if cards_str[i] == "" and not all([x == "" for x in cards_list]):
                cards_str[i] = cards_list.pop()
                cards_file[i] = img_dir + cards_str[i] + ".png"
                cards_image[i] = pygame.transform.rotozoom(pygame.image.load(cards_file[i]), 0, scale)


        SURFACE.fill((surfacecolor))
        #カードカウントの表示
        cards_count_p = pay_c_font.render(str(cards_count),True,fontcolor)
        SURFACE.blit(cards_count_p,count_xy)
        #枠表示
        pygame.draw.rect(SURFACE, pay_c_fontcolor_y, count_fra_xy,2)           # 黄色い枠

        # カードの表示
        for i,v in enumerate(cards_str):
            if i == 0:  # センターカード
                SURFACE.blit(cards_image[0], cards_xy[0])
            elif (cards_str[0][0:1] == cards_str[i][0:1]) or (cards_str[0][1:] == cards_str[i][1:]): #手札が出せる場合
                cards_ok[i] = 1
                SURFACE.blit(cards_image[i], cards_xy[i])
                pygame.draw.rect(SURFACE, line_c, cards_xy[i], 3)   # 枠を表示
            elif v != "":                                # 手札が出せないが、存在する場合
                cards_ok[i] = 0
                SURFACE.blit(cards_image[i], cards_xy[i])
            elif v == "":
                cards_ok[i] = 0

        orbit = cards_count // 52 + 1

        #選択可能なカードがあるか判定
        if 1 in cards_ok:
            message = "カードを選択してください"
            #message = "まだカードがあります。" + str(orbit) + "巡目です。"
            if orbit == 2 and cards_count == 104:
                message = "Congratulations! Cool 104!!"
        else:
            message = "ゲームオーバー"

        #マウスのクリック位置を取得
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:  # 左クリック
            cur_x, cur_y = pygame.mouse.get_pos()
            # ■マウスカーソル位置把握のためのメッセージ（後で削除）
            # message = str(cur_x) + "," + str(cur_y)
            # マウスのクリック座標が手札の範囲か検証
            for i, v in enumerate(cards_xy):
                if cards_xy[i].collidepoint(cur_x, cur_y):
                    select_card = i
                    time.sleep(0.2)

                    # マウスのクリック範囲が有効なカードの場合、センターカードを置き換える
                    if cards_ok[select_card] == 1 and cards_str[i] != "":
                        cards_str[0] = cards_str[select_card]
                        cards_file[0] = img_dir + cards_str[0] + ".png"
                        cards_image[0] = pygame.transform.rotozoom(pygame.image.load(cards_file[0]), 0, scale)
                        cards_str[i] = ""
                        # カウンターをアップ
                        cards_count += 1
                        break
        # メッセージ表示
        game_message = sysfont.render(message,True,fontcolor)
        #SURFACE.blit(game_message, (disp_card_spa * 2 + card_width * 2, 400))
        SURFACE.blit(game_message, (card_width * 2, 400))

        # 使用カード背景表示
        pygame.draw.rect(SURFACE, pay_c_fontcolor_b, pay_back_xy)             # 黒い四角


        # 使用カード表示
        SURFACE.blit(pay_Mark_s, (pay_c_x,pay_c_y + pay_c_line * 0,100,100))
        SURFACE.blit(pay_Mark_h, (pay_c_x,pay_c_y + pay_c_line * 1,100,100))
        SURFACE.blit(pay_Mark_c, (pay_c_x,pay_c_y + pay_c_line * 2,100,100))
        SURFACE.blit(pay_Mark_d, (pay_c_x,pay_c_y + pay_c_line * 3,100,100))
        pay_c_list = cards.payout_list(cards_str[0],"")

        for i, v in enumerate(pay_c_list):
            v = pay_c_list[i][1:]
            if v == "1":
                chr = "A"
            elif v == "10":
                chr = "X"
            elif v == "11":
                chr = "J"
            elif v == "12":
                chr = "Q"
            elif v == "13":
                chr = "K"
            else:
                chr = pay_c_list[i][1:]
            if pay_c_list[i][0:1] == "s":
                chr_disp = sysfont.render(chr, True, pay_c_fontcolor_w)
                SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 0))
                if pay_c_list[i] in cards_str[1:]:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_y)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 0))
                elif pay_c_list[i] not in cards_str[1:] and pay_c_list[i] not in cards_list:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_b)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 0))
            elif pay_c_list[i][0:1] == "h":
                chr_disp = sysfont.render(chr, True, pay_c_fontcolor_w)
                SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 1))
                if pay_c_list[i] in cards_str[1:]:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_y)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 1))
                elif pay_c_list[i] not in cards_str[1:] and pay_c_list[i] not in cards_list:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_b)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 1))
            elif pay_c_list[i][0:1] == "c":
                chr_disp = sysfont.render(chr, True, pay_c_fontcolor_w)
                SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 2))
                if pay_c_list[i] in cards_str[1:]:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_y)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 2))
                elif pay_c_list[i] not in cards_str[1:] and pay_c_list[i] not in cards_list:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_b)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 2))
            elif pay_c_list[i][0:1] == "d":
                chr_disp = sysfont.render(chr, True, pay_c_fontcolor_w)
                SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 3))
                if pay_c_list[i] in cards_str[1:]:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_y)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 3))
                elif pay_c_list[i] not in cards_str[1:] and pay_c_list[i] not in cards_list:
                    chr_disp = sysfont.render(chr, True, pay_c_fontcolor_b)
                    SURFACE.blit(chr_disp, (pay_c_x + pay_c_buf + pay_c_spa * (i % 13), pay_c_y + pay_c_line * 3))

        # 使用カード枠表示
        pygame.draw.rect(SURFACE, pay_c_fontcolor_y, pay_back_xy,2)           # 黄色い枠

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        #1秒に10回描画
        FPSCLOCK.tick(10)

if __name__ == "__main__":
    main()

