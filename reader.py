from tkinter import *

from PIL import Image, ImageTk


class reader:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1600x920")
        self.root.title("emm")
        f1 = open('data.txt', encoding='utf-8')
        self.length = int(f1.readline().split(' ')[0])
        self.count = 0
        self.command = {}
        for i in range(0, self.length + 1):
            temp = f1.readline()
            self.command[i] = temp
        self.reader()
        self.root.mainloop()

    def resize(self, pil_image):
        """
        resize a pil_image object so it will fit into
         a box of size w_box times h_box, but retain aspect ratio
        对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
        """

        w, h = pil_image.size
        w_box = 700
        h_box = 700
        f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        # print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def reader(self):
        """定义frame长宽"""
        global bg, body, face, ttext, name
        width = 1600
        height = 700
        for i in range(0, 3):
            temp = self.command[i].split(' ')
            if temp[0] == "setbody":
                if int(temp[1]) == 1:
                    self.body1 = ImageTk.PhotoImage(self.resize(Image.open(temp[2])))
                    self.count += 1
                    self.body_amount = 1
                if int(temp[1]) == 2:
                    self.body1 = ImageTk.PhotoImage(self.resize(Image.open(temp[2])))
                    self.body2 = ImageTk.PhotoImage(self.resize(Image.open(temp[3])))
                    self.body_amount = 2
                    self.count += 1
            if temp[0] == "setbg":
                self.bg = PhotoImage(file=temp[1])
                self.count += 1
            if temp[0] == "show":
                print(temp)
                print(self.command)
                self.face = PhotoImage(file=temp[1])
                self.name = temp[2].split(':')[0]
                self.context = temp[2].split(':')[1]
                self.count += 1
        app1 = Frame(self.root, width=width, height=height)
        app1.grid()
        "建立画布并放入图片，最后用grid打包"
        self.canvas1 = Canvas(app1, width=width, height=height)
        self.cbg = self.canvas1.create_image(800, 350, image=self.bg)
        self.cbody1 = self.canvas1.create_image(350, 350, image=self.body1)
        if self.body_amount == 2:
            self.cbody2 = self.canvas1.create_image(700, 350, image=self.body1)
        self.canvas1.grid()
        "创建新的frame，并创建画布，放入图片并打包"
        app2 = Frame(self.root, width=width, height=200)
        app2.grid()
        self.canvas2 = Canvas(app2, width=300, height=200, bg='grey')
        self.canvas2.grid(row=0, column=0)
        self.cface = self.canvas2.create_image(150, 100, image=self.face)
        "文本框创建以及打包"
        self.text = Text(app2, width=100, height=10, font=10)
        self.text.grid(row=0, column=4, columnspan=10)
        self.text.insert(0.0, self.name + ':' + self.context)
        Button(app2, text='我是按钮', width=30, height=10,
               command=lambda: self.resume()).grid(
            row=0, column=15)

    def update_canvas1(self, canvas1):
        canvas1.delete(ALL)

    def resume(self):
        temp = self.command[self.count].split(' ')
        if temp[0] == "setbody":
            if int(temp[1]) == 1:
                self.body1 = ImageTk.PhotoImage(self.resize(Image.open(temp[2])))
                self.canvas1.delete(self.cbody1)
                if self.body_amount == 2:
                    self.canvas1.delete(self.cbody2)
                    self.body_amount = 1
                self.cbody1 = self.canvas1.create_image(350, 350, image=self.body1)
                self.count += 1
            if int(temp[1]) == 2:
                self.body1 = ImageTk.PhotoImage(self.resize(Image.open(temp[2])))
                self.body2 = ImageTk.PhotoImage(self.resize(Image.open(temp[3])))
                self.canvas1.delete(self.cbody1)
                if self.body_amount == 2:
                    self.canvas1.delete(self.cbody2)
                    self.body_amount = 2
                self.cbody1 = self.canvas1.create_image(350, 350, image=self.body1)
                self.cbody2 = self.canvas1.create_image(1350, 350, image=self.body2)
                self.count += 1
            self.resume()
        if temp[0] == "setbg":
            self.canvas1.delete(self.cbg)
            self.bg = PhotoImage(file=temp[1])
            self.cbg = self.canvas1.create_image(800, 350, image=self.bg)
            self.count += 1
            self.resume()
        if temp[0] == "show":
            print(temp)
            print(self.command)
            self.face = PhotoImage(file=temp[1])
            self.name = temp[2].split(':')[0]
            self.context = temp[2].split(':')[1]
            self.canvas2.delete(ALL)
            self.cface = self.canvas2.create_image(150, 100, image=self.face)
            self.text.delete('1.0', 'end')
            self.text.insert(0.0, self.context)
            self.text.insert(0.0, self.name + ':')
            self.cfaceis = TRUE
            self.count += 1
        if temp[0] == 'change':
            self.body1 = ImageTk.PhotoImage(self.resize(Image.open(temp[1])))
            self.canvas1.delete(self.cbody1)
            self.cbody1 = self.cbody1 = self.canvas1.create_image(350, 350, image=self.body1)
            self.count += 1
            self.resume()
        if temp[0] == 'aside':
            if self.cfaceis == TRUE:
                self.canvas2.delete(self.cface)
            self.text.delete('1.0', 'end')
            self.text.insert(0.0, temp[1])
        self.root.update()
