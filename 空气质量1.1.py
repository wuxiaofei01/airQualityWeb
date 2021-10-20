from abc import abstractproperty
import matplotlib.pyplot as plt
import urllib
import urllib.request
from xpinyin import Pinyin
import tkinter as tk
from PIL import Image, ImageTk


def getId(city):
    url = "https://website-api.airvisual.com/v1/routes/china/" + city
    f = urllib.request.urlopen(url)
    data = f.read()
    f.close()
    data = data.decode("utf-8")
    b = eval(data)
    return b['id']


def drawPie(x):
    plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    label = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']  # 定义饼图的标签，标签是列表
    explode = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]  # 设定各项距离圆心n个半径
    # plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    plt.pie(x, explode=explode, labels=label,
            autopct='%1.1f%%')  # 绘制饼图
    plt.title('aqi')  # 绘制标题
    # plt.savefig('./20')  # 保存图片
    plt.show()


def drawColumn(x):
    label = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']  # 定义饼图的标签，标签是列表
    plt.bar(label, x, 0.4, color="red")
    plt.xlabel("pollutantName")
    plt.ylabel("concentration")
    plt.title("api")
    plt.show()


def getMes():
    p = Pinyin()

    city = p.get_pinyin(text1.get())
    city = city.replace('-', '')
    print(city)
    id = getId(city)
    url = "https://website-api.airvisual.com/v1/cities/" + id
    f = urllib.request.urlopen(url)
    data = f.read()
    f.close()
    data = data.decode("utf-8")
    data = eval(data)

    print(data['current']['pollutants'], type(data['current']['pollutants']))
    index = 0
    x = []
    for i in data['current']['pollutants']:
        dic = data['current']['pollutants'][index]
        print("api is : %d" % dic['aqi'], end="\t")
        print("concentration is %d:" % dic["concentration"], end="\t")
        print("pollutantName is :" + dic["pollutantName"], end="\n")
        index = index+1
        x.append(dic['aqi'])
        pass
    # drawPie(x)
    drawColumn(x)


def get_image(file_nam, width, height):  # 获取图片 以及像素大小
    im = Image.open(file_nam).resize((width, height))
    return ImageTk.PhotoImage(im)


win = tk.Tk()
win.title('全国各地空气质量查询系统')
win.geometry('500x500')
# 画布  设置背景图片
canvas = tk.Canvas(win, height=500, width=500)
im_root = get_image('C:/Users/13376/Pictures/2.jpeg', width=500, height=500)
canvas.create_image(250, 250, image=im_root)
canvas.pack()


# 单行文本  标题
L1 = tk.Label(win, bg='yellow', text="地区：", font=("SimHei", 12))
L1.place(x=85, y=100)
# 单行文本框  可采集键盘输入
text1 = tk.Entry(win, font=("SimHei", 12), show=None, width=35)  # 城市
text1.place(x=140, y=100)

button1 = tk.Button(win, bg='red', text="单次查询",
                    width=25, height=1, command=getMes)
button1.place(x=160, y=200)


# 设置多行文本框  宽 高  文本框中字体  选中文字时文字的颜色
t = tk.Text(win, width=30, height=8, font=(
    "SimHei", 18), selectforeground='red')  # 显示多行文本
t.place(x=70, y=280)


# 进入消息循环
win.mainloop()
