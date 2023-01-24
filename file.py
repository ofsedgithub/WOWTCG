import json
from tkinter import messagebox


class Cards:
    def __init__(self):
        f1, f2, f3 = open('resource\\cards\\cards_owned.json', 'r'), open('resource\\cards\\cards_used.json', 'r'),\
                    open('resource\\cards\\cards_name.json', 'r')
        self.cards_owned, self.cards_used, self.cards_name = json.load(f1), json.load(f2), json.load(f3)
        self.check_inputs()

    def check_inputs(self):
        len1 = self.cards_owned.__len__()
        len2 = self.cards_used.__len__()
        len3 = self.cards_name.__len__()
        if len1 > len3 or len2 > len1 or len2 > 60:
            messagebox.showerror('??!!', '你小子作弊是吧')
        self.cards_owned, self.cards_used = [], []


Cards()
