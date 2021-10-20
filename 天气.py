import requests
from lxml import etree
import re
import tkinter as tk
from PIL import Image, ImageTk
from xpinyin import Pinyin
import datetime
import matplotlib.pyplot as plt


def get_image(file_nam, width, height):  # 获取图片 以及像素大小
    im = Image.open(file_nam).resize((width, height))
    return ImageTk.PhotoImage(im)


def getWeatherOne():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        "referer": "https://lishi.tianqi.com"
    }
    p = Pinyin()
    place = ''.join(p.get_pinyin(text1.get()).split('-')
                    )           # 获取地区文本框的输入  变为拼音
    date = text2.get()   # 获取时间文本框的输入
    if '/' in date:
        tm_list = date.split('/')
    elif '-' in date:
        tm_list = date.split('-')
    else:
        tm_list = re.findall(r'\d+', date)
    if int(tm_list[1]) < 10:       # 1-9月  前面加 0
        tm_list[1] = f'0{tm_list[1]}'

    # 分析网页规律  构造url
    # 直接访问有该月所有天气信息的页面 提高查询效率
    url = f"https://lishi.tianqi.com/{place}/{''.join(tm_list[:2])}.html"
    print(url)
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    print(html)
    # xpath定位提取该日天气信息
    info = html.xpath(f'//ul[@class="thrui"]/li[{int(tm_list[2])}]/div/text()')
    # 输出信息格式化一下
    print(info)
    info1 = ['日期：', '最高气温：', '最低气温：', '天气：', '风向：']
    datas = [i + j for i, j in zip(info1, info)]
    info = '\n'.join(datas)
    t.delete(1.0, 'end')
    t.insert('insert', '        查询结果如下        \n\n')
    t.insert('insert', info)


def getWeatherMore():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        "referer": "https://lishi.tianqi.com"
    }
    p = Pinyin()
    place = ''.join(p.get_pinyin(text1.get()).split('-')
                    )           # 获取地区文本框的输入  变为拼音

    date = text2.get()   # 获取时间文本框的输入
    if '/' in date:
        tm_list = date.split('/')
    elif '-' in date:
        tm_list = date.split('-')
    else:
        tm_list = re.findall(r'\d+', date)
    if int(tm_list[1]) < 10:       # 1-9月  前面加 0
        tm_list[1] = f'0{tm_list[1]}'
    # 然后需要往前推7天 得到分别的最高和最低气温
    in_date = "-".join(tm_list)  # 保存的查询当天的日期      转换格式得到正确的格式

    maxTemperature = []
    minTemperature = []
    for i in range(1, 8):
        dt = datetime.datetime.strptime(in_date, "%Y-%m-%d")
        out_date = (dt + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
        if '/' in out_date:
            tm_list = out_date.split('/')
        elif '-' in out_date:
            tm_list = out_date.split('-')
        else:
            tm_list = re.findall(r'\d+', out_date)
        if int(tm_list[1]) < 10:       # 1-9月  前面加 0
            tm_list[1] = f'0{tm_list[1]}'
        # 然后需要往前推7天 得到分别的最高和最低气温
        # 分析网页规律  构造url
        # 直接访问有该月所有天气信息的页面 提高查询效率
        url = f"https://lishi.tianqi.com/{place}/{''.join(tm_list[:2])}.html"
        resp = requests.get(url, headers=headers)
        html = etree.HTML(resp.text)
        # xpath定位提取该日天气信息
        info = html.xpath(
            f'//ul[@class="thrui"]/li[{int(tm_list[2])}]/div/text()')
        # 输出信息格式化一下
        maxTemperature.append(info[1])
        minTemperature.append(info[2])

    print(maxTemperature)
    line1 = []
    line2 = []
    x = [-6, -5, -4, -3, -2, -1, 0]
    for i in maxTemperature:
        if len(i) == 2:
            str = i[:1]
            line1.append(int(str))
        else:
            str = i[:2]
            line1.append(int(str))

    for i in minTemperature:
        if len(i) == 2:
            str = i[:1]
            line2.append(int(str))
        else:
            str = i[:2]
            line2.append(int(str))

    plt.plot(x, line1, marker='o', mec='r', mfc='w', label=u'最高气温曲线图')
    plt.plot(x, line2, marker='*', ms=10, label=u'y=x^3曲线图')
    plt.show()


win = tk.Tk()
win.title('全国各地历史天气查询系统')
win.geometry('500x500')
# 画布  设置背景图片
canvas = tk.Canvas(win, height=500, width=500)
im_root = get_image('C:/Users/13376/Pictures/2.jpeg', width=500, height=500)
canvas.create_image(250, 250, image=im_root)
canvas.pack()
# 单行文本  标题
L1 = tk.Label(win, bg='yellow', text="地区：", font=("SimHei", 12))
L2 = tk.Label(win, bg='yellow', text="时间：", font=("SimHei", 12))
L1.place(x=85, y=100)
L2.place(x=85, y=150)
# 单行文本框  可采集键盘输入
text1 = tk.Entry(win, font=("SimHei", 12), show=None, width=35)  # 城市
text2 = tk.Entry(win, font=("SimHei", 12), show=None, width=35)  # 时间
text1.place(x=140, y=100)
text2.place(x=140, y=150)
# 设置查询按钮
button1 = tk.Button(win, bg='red', text="单次查询",
                    width=25, height=1, command=getWeatherOne)
button1.place(x=160, y=200)

button2 = tk.Button(win, bg='red', text="查询过去七天趋势",
                    width=25, height=1, command=getWeatherMore)
button2.place(x=160, y=240)

# 设置多行文本框  宽 高  文本框中字体  选中文字时文字的颜色
t = tk.Text(win, width=30, height=8, font=(
    "SimHei", 18), selectforeground='red')  # 显示多行文本
t.place(x=70, y=280)


# 进入消息循环
win.mainloop()
