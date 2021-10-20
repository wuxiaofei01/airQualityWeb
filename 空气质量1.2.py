import tkinter as tk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import urllib
import urllib.request
from xpinyin import Pinyin
import tkinter as tk
from PIL import Image, ImageTk


matplotlib.use('TkAgg')
root = Tk()
root.title("tkinter and matplotlib")
f = Figure(figsize=(6, 6), dpi=100)  # figsize定义图像大小，dpi定义像素
f_plot = f.add_subplot(111)  # 定义画布中的位置


def getId(city):
    url = "https://website-api.airvisual.com/v1/routes/china/" + city
    f = urllib.request.urlopen(url)
    data = f.read()
    f.close()
    data = data.decode("utf-8")
    b = eval(data)
    return b['id']


def getMes():  # 返回列表 是x轴
    p = Pinyin()
    city1 = p.get_pinyin(text1.get())
    city1 = city1.replace('-', '')

    city2 = p.get_pinyin(text2.get())
    city2 = city2.replace('-', '')

    id = getId(city1 +'/'+ city2)  # 获取城市的id
    # id = "iYxbif49rJQTBFfCe"
    url = "https://website-api.airvisual.com/v1/cities/" + id + "/measurements"
    f = urllib.request.urlopen(url)
    data = f.read()
    f.close()
    data = data.decode("utf-8")
    data = eval(data)

    dataList = []
    j = 0
    for i in data['measurements']['hourly']:
        # print(i,end='\n')
        if j % 10 == 0:
            dataList.append(i)
        j = j + 1
    time = []
    aqi = []
    pm25 = []
    pm10 = []
    o3 = []
    no2 = []
    so2 = []
    co = []
    for i in dataList:
        dataDict = i
        time.append(dataDict['ts'])
        aqi.append(dataDict['aqi'])
        pm25.append(dataDict['pm25'])
        pm10.append(dataDict['pm10'])
        o3.append(dataDict['o3'])
        no2.append(dataDict['no2'])
        so2.append(dataDict['so2'])
        co.append(dataDict['co'])
    return time, aqi, pm25, pm10, o3, no2, so2, co


def get_image(file_nam, width, height):  # 获取图片 以及像素大小
    im = Image.open(file_nam).resize((width, height))
    return ImageTk.PhotoImage(im)


def drawColumn(x):
    f_plot.clear()
    label = ['aqi', 'pm25', 'pm10', 'o3', 'no2', 'so2', 'co']  # 定义饼图的标签，标签是列表
    f_plot.bar(label, x, 0.4, color="red")
    f_plot.set_title('api')
    f_plot.set_ylabel('concentration')
    f_plot.set_xlabel('pulutionName')

    canvs.draw()


def drawLine(time, aqi, pm25, pm10, o3, no2, so2, co):
    f_plot.clear()

    j = 0
    timeDate = []
    pm25Data = []
    pm10Data = []
    o3Data = []
    no2Data = []
    so2Data = []
    coData = []
    for i in pm25:
        timeDate.append(time[j][5:13])
        pm25Data.append(pm25[j]['aqi'])
        pm10Data.append(pm10[j]['aqi'])
        o3Data.append(o3[j]['aqi'])
        no2Data.append(no2[j]['aqi'])
        so2Data.append(so2[j]['aqi'])
        coData.append(co[j]['aqi'])
        j += 1

    f_plot.plot(timeDate, aqi, color='blue', linewidth=3.0,
                linestyle='-.', Label='aqi')
    f_plot.plot(timeDate, pm25Data, color='red', linewidth=3.0,
                linestyle='-.', Label='pm25')
    f_plot.plot(timeDate, pm10Data, color='green', linewidth=3.0,
                linestyle='solid', Label='pm10')
    f_plot.plot(timeDate, o3Data, color='black', linewidth=3.0,
                linestyle='-.', Label='o3')
    f_plot.plot(timeDate, no2Data, color='purple', linewidth=3.0,
                linestyle='dotted', Label='no2')
    f_plot.plot(timeDate, so2Data, color='yellow', linewidth=3.0,
                linestyle='-.', Label='so2')
    f_plot.plot(timeDate, coData, color='pink', linewidth=3.0,
                linestyle='-', Label='co')

    f_plot.set_title('api')
    f_plot.set_ylabel('concentration')
    f_plot.set_xlabel('pulutionName')

    f_plot.legend(['aqi', 'pm25', 'pm10', 'o3',
                  'no2', 'so2', 'co'], fontsize='13')
    canvs.draw()


def buttonOne():
    time, aqi, pm25, pm10, o3, no2, so2, co = getMes()
    drawLine(time, aqi, pm25, pm10, o3, no2, so2, co)


def buttonTwo():
    time, aqi, pm25, pm10, o3, no2, so2, co = getMes()
    print(0)
    x = []
    x.append(aqi[-1])
    x.append(pm25[-1]['concentration'])
    x.append(pm10[-1]['concentration'])
    x.append(o3[-1]['concentration'])
    x.append(no2[-1]['concentration'])
    x.append(so2[-1]['concentration'])
    x.append(co[-1]['concentration'])
    drawColumn(x)


canvs = FigureCanvasTkAgg(f, root)  # f是定义的图像，root是tkinter中画布的定义位置
canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
Button(root, text='过去一周空气质量', command=buttonOne).pack()
Button(root, text='当前时间空气质量', command=buttonTwo).pack()

# 单行文本  标题
L1 = tk.Label(root, bg='yellow', text="省市：", font=("SimHei", 12))
L1.place(x=85, y=600)

L2 = tk.Label(root, bg='yellow', text="市区：", font=("SimHei", 12))
L2.place(x=85, y=620)

# 单行文本框  可采集键盘输入
text1 = tk.Entry(root, font=("SimHei", 12), show=None, width=10)  # 城市
text1.place(x=140, y=600)

text2 = tk.Entry(root, font=("SimHei", 12), show=None, width=10)  # 城市
text2.place(x=140, y=620)

root.mainloop()
