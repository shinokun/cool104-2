"""リストを作成"""
def payout_list(card_0_num,mode) -> object:
    """
    :rtype: object
    """
    import random
    import copy
    import pygame
    cards_org = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13',
                 'h1','h2','h3','h4','h5','h6','h7','h8','h9','h10','h11','h12','h13',
                 'c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13',
                 'd1','d2','d3','d4','d5','d6','d7','d8','d9','d10','d11','d12','d13']
    #cards_org = ['s2','d1','h1','c1','s1','d1']
    #cards_org = random.sample(cards_org, len(cards_org))

    if mode == 1:
        while True:
            cards_str = [""] * 6
            if card_0_num != "":
                cards_str[0] = card_0_num
            # カードリストをランダムに払い出す
            cards_list = random.sample(cards_org, len(cards_org))
            #リストの保存
            cards_list_back = copy.deepcopy(cards_list)
            # カードを１枚ずつ配列にセットする
            for i, v in enumerate(cards_str):
                if cards_str[i] != "":
                    continue
                else:
                    cards_str[i] = cards_list.pop()

            #  cards_str[0]の「数字」部位を設定する
            tmp = cards_str[0][1:]
            #  cards_str[1:]の「数字」部位を設定する
            tmp2 = []
            for p in range(1, 6):
                tmp2.append(cards_str[p][1:])
                p += 1
            # cards_str[1:]の中に、cards_str[0]と同じ「マーク」または「数字」が２つ以上含まれるか確認する
            num = sum(list(map(lambda x: cards_str[0][0] in x, cards_str[1:]))) + sum(list([1 if tmp == tmp2[z] else 0 for z in range(5)]))
            # cards_str[1:]の中に、cards_str[0]と同じ「マーク」または「数字」が２つ以上含まれる場合は、ループを抜ける
            if num > 2:
                break
        return cards_list_back
    else:
        return cards_org




