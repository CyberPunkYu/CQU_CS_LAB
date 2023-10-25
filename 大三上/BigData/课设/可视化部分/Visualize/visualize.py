from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from pyecharts import options as opts
from pyecharts.charts import Pie, Line, ThemeRiver

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

SAVAPATH = ''  # 可视化图片存储位置，需自己添加

def save_picture(file_name='render.html', output_name='result.png', is_remove_html=False):
    '''渲染成图片
    :param file_name: 网页名
    :param output_name: 渲染图片名
    :param is_remove_html: 是否删除网页
    :return:
    '''
    make_snapshot(snapshot, file_name, output_name, is_remove_html=is_remove_html)
class visualize:
    
    def drawLine(self, key_list, value_list1, value_list2, value_list3):
        '''
        绘制折线图
        param key_list: 键，横坐标值 ['x1', 'x2', 'x3', ..., 'xn']
        param value_listi: 值，纵坐标值，分别传入B站弹幕，B站评论和知乎评论情感指数数据 [num1, num2, num3, ..., numn]
        '''
        line = (Line(
                     init_opts=opts.InitOpts(
                                             theme='light',
                                             bg_color = 'white'
                                             )
                    )
                .add_xaxis(key_list)
                .add_yaxis('B站弹幕', value_list1)
                .add_yaxis('B站评论', value_list2)
                .add_yaxis('知乎评论', value_list3)
                .set_global_opts(
                                title_opts=opts.TitleOpts(title='情感指数折线图'),
                                yaxis_opts=opts.AxisOpts(
                                                        min_ = 0,
                                                        max_ = 1
                                                        ),
                                xaxis_opts=opts.AxisOpts(
                                                        name = '时间/季度'
                                                        ),
                                legend_opts=opts.LegendOpts(
                                                           is_show = True,
                                                           legend_icon='circle'
                                                           )
                                )
                )
        line.render('line.html')
        save_picture('line.html', SAVAPATH + '情感指数折线可视化.png')
        print("折线可视化生成成功")

    def drawRiver(self, cate, data, name):
        '''
        绘制弹幕河流图
        param cate: 弹幕种类，此处为positive和negative ['Positive', 'Negative']
        param data: 数据部分，[[TIME, num, cate[i]], [TIME, num, cate[i]]]
        param name: 图保存名字
        '''
        river = (ThemeRiver(
                            init_opts=opts.InitOpts(
                                             theme='light',
                                             bg_color = 'white'
                                             )
                            )
                .add(
                    series_name = cate,
                    data = data,
                    singleaxis_opts=opts.SingleAxisOpts(pos_top="50", pos_bottom="50", type_="time")
                    )
                .set_global_opts(
                                title_opts=opts.TitleOpts(title=name + '弹幕分布河流图'),
                                xaxis_opts=opts.AxisOpts(
                                                        name = '时间/季度'
                                                        )
                                )
                )

        river.render('river.html')
        save_picture('river.html', SAVAPATH + name + '弹幕分布河流可视化.png')
        print("河流可视化生成成功")

    def drawPie(self, key_list, value_list, name):
        '''
        情感趋向南丁格尔玫瑰图
        param key_list: 键，横坐标值 ['x1', 'x2', 'x3', ..., 'xn']
        param value_list: 值，纵坐标值，评论情感趋向指数数据 [num1, num2, num3, ..., numn]
        param name: 图保存名字
        '''
        pie = (Pie(
                     init_opts=opts.InitOpts(
                                             theme='light',
                                             bg_color = 'white'
                                             )
                    )
                .add("", [list(a) for a in zip(key_list, value_list)], rosetype="area")
                .set_global_opts(
                                title_opts=opts.TitleOpts(title=name + '情感趋势南丁格尔玫瑰图'),
                                legend_opts=opts.LegendOpts(
                                                           is_show = True,
                                                           pos_left='80%',
                                                           orient='vertical'
                                                           )
                                )
                )
        pie.render('pie.html')
        save_picture('pie.html', SAVAPATH + name + '情感趋势南丁格尔玫瑰图可视化.png')
        print("饼图可视化生成成功")