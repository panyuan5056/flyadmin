from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import ChartType


init_opts=opts.InitOpts(
            #设置宽度、高度
            width='100%',
            height='300px'
        )

def gauge(title, x= [("完成率", 66.6)]):
    xx = Gauge(init_opts=init_opts).add("", x, radius="50%").set_global_opts(title_opts=opts.TitleOpts(title=title)).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def kine(title, x, y):
    xx = Kline(init_opts=init_opts).add_xaxis(x).add_yaxis("kline", y).set_global_opts(
                yaxis_opts=opts.AxisOpts(is_scale=True),
                xaxis_opts=opts.AxisOpts(is_scale=True),
                title_opts=opts.TitleOpts(title=title),
            ).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def wordcloud(name, value):
    wordcloud = WordCloud(init_opts=init_opts)
    wordcloud.add("", name, value, word_size_range=[ 20, 100])
    xx =wordcloud.render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def bar(title, names, values):
    b = Bar(init_opts=init_opts).add_xaxis(names)
    b.add_yaxis("", [values.get(name,0) for name in names])
    b.set_global_opts(title_opts=opts.TitleOpts(title=""))
    xx = b.render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def bar3d(title, x, y, data):
    xx = (
            Bar3D(init_opts=init_opts)
            .add(
                "",
                data,
                xaxis3d_opts=opts.Axis3DOpts(x, type_="category"),
                yaxis3d_opts=opts.Axis3DOpts(y, type_="category"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            ).set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=20),
                title_opts=opts.TitleOpts(title=""),
            )
        ).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def boxplot(title, x, y):
    c = Boxplot(init_opts=init_opts)
    c.add_xaxis(x)
    for key, v in y.items():
        c = c.add_yaxis(key, c.prepare_data(v))
    c = c.set_global_opts(title_opts=opts.TitleOpts(title=title))
    xx = c.render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def funnel(title, subtitle, x, y):
    xx =  Funnel(init_opts=init_opts).add(subtitle, [list(z) for z in zip(x, y)]).set_global_opts(title_opts=opts.TitleOpts(title=title)).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def geo(title, subtitle, x, y):
    xx = Geo().add_schema(maptype="china").add(
            subtitle,
            [list(z) for z in zip(x, y)],
            type_=ChartType.EFFECT_SCATTER,
        ).set_series_opts(label_opts=opts.LabelOpts(is_show=False)).set_global_opts(title_opts=opts.TitleOpts(title=title)).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def graph_base(title, nodes=[{"name": "结点1", "symbolSize": 10}]):
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get("name"), "target": j.get("name")})
    
    xx = Graph(init_opts=init_opts).add("", nodes, links, repulsion=8000).set_global_opts(title_opts=opts.TitleOpts(title=title)).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)
    
def heatmap(title, subtitle, x, y_title, y_x, y_y):
    xx = HeatMap(init_opts=init_opts).add_xaxis(x).add_yaxis(y_title, y_x, y_y).set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        visualmap_opts=opts.VisualMapOpts(),
    ).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)


def line(title, x, y):
    line =  Line(init_opts=init_opts).add_xaxis(x)
    for key, v in y.items():
        line = line.add_yaxis(key, v)
    line = line.set_global_opts(title_opts=opts.TitleOpts(title=""))
    xx = line.render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def liquid(title, x, y=[]):
    xx = Liquid(init_opts=init_opts).add(x, y).set_global_opts(title_opts=opts.TitleOpts(title=title)).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)

def pie(title, x, y):
    xx =  Pie(init_opts=init_opts).add("", [list(z) for z in zip(x, y)]).set_global_opts(title_opts=opts.TitleOpts(title="")).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)
 

def radar(title, x, y):
    c = Radar(init_opts=init_opts)
    schemas = []
    for x1, v in x:
        schemas.append(opts.RadarIndicatorItem(name=x1, max_=v))
    c = c.add_schema(schema=schemas)
    for y1, v in y:
        c = c.add(y1, v)
        
    c = c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    xx = c.set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="single"),
        title_opts=opts.TitleOpts(title=title),
    ).render_embed()
    return '''<div class="el-card box-card is-always-shadow" style="margin:10px"><div class="el-card__header"><div class="clearfix"><span>{}</span></div></div>
            <div class="el-card__body">{}</div></div>'''.format(title, xx)
     