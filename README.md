# flyadmin

# 基于Simple UI做的二次开发，具体使用方法请查看Simple UI
# 该项目主要用于项目的管理功能，新增的图标和自定义组件大致可以覆盖简单管理项目的80%的功能

# 新增了基于pyecharts图表支持
    # 使用方法：from flyadmin.views.charts import bar, pie, line, kine, wordcloud, bar, bar3d, boxplot, # # funnel, graph_base 等
    # 详情请看 flyadmin/views/charts.py文件
    
    # demo1
    from django.db import models
    from flyadmin.views.charts import bar, pie, line

    class Assets(models.Model):
        name          = models.CharField("名称", max_length=200)
        ip            = models.GenericIPAddressField()
        category      = models.CharField("类型", max_length=200)
        create_time   = models.DateTimeField("创建时间",auto_now=True)  
        update_time   = models.DateTimeField("更新时间",auto_now_add=True) 

        def __str__(self):
            return self.name
            
        class Meta:
            verbose_name = '资产管理'
            verbose_name_plural = '资产管理'

        @classmethod
        def show_plots(cls):
            result = []
            assets = cls.objects.all()
            xx = {}
            for asset in assets:
                if xx.get(asset.category):
                    xx[asset.category] += 1 
                else:
                    xx[asset.category] = 1
            result.append({
                'size':8,
                'plot':bar('数据分布', list(set([i.category for i in assets])), xx)
                })
            return result


    # demo2
    import psutil
    from datetime import datetime as dt
    from django.shortcuts import render
    from django.contrib import admin
    from django.conf import settings
    from django import forms
    from django.apps import apps
    from .models import Natural
    from django.urls import path
    from pyecharts import options as opts
    from flyadmin.views.charts import bar, pie, line

    class NaturalAdmin(admin.ModelAdmin):
        model = Natural

        def admin_view_natural(self, request):
            _f1 = lambda x:round(x/1024/1024/1024, 1)
            #将数据写入到里面来到首页数据里(不得修改)
            mem     = psutil.virtual_memory()
            #cpu     = psutil.cpu_percent()
            disk    = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            naturals = Natural.objects.order_by('create_time').all()
            
            c = line('cpu趋势(G)', [i.create_time.strftime('%Y-%m-%d %H') for i in naturals], {'占用比率':[i.ava for i in naturals]})
            p = pie("内存占比(G)", ('全部','可用'), (_f1(mem.total), _f1(mem.available)))
            d = pie("硬盘占比(G)", ('全部','使用', '可用'), (_f1(disk.total), _f1(disk.used), _f1(disk.free)))
            n = pie("网络情况(G)", ('接收','发送'), (_f1(network.bytes_recv), _f1(network.bytes_sent)))
            html = ['<el-row><div class="grid-content">']
            html.append('<div class="el-col el-col-8">{}</div>'.format(p))
            html.append('<div class="el-col el-col-8">{}</div>'.format(d))
            html.append('<div class="el-col el-col-8">{}</div>'.format(n))
            html.append('</div></el-row>')
            html.append('<el-row><div class="grid-content"><div class="el-col el-col-24">{}</div></div></el-row>'.format(c))
            xplots = ''.join(html)   
            return render(request, "admin/xplots.html", locals()) 
    
        def changelist_view(self, request, extra_content=None):
            return self.admin_view_natural(request)

        admin.site.register(Natural, NaturalAdmin)

        


# 新增了一批自定义的form支持
    #from flyadmin.widget.forms import SelectBoxWidget, TimelineWidget, EditorWidget, DateTimeWidget, UploadImagesWidget, InputNumberWidget, UploadFileWidget, StepsWidget, StepsNormalWidget
    
    # 详情请看 flyadmin/widget/forms.py文件
    # demo1
    from django import forms
 
    class CommentForm(forms.Form):
        name = forms.CharField()
        url = forms.URLField()
        comment = forms.CharField(widget=forms.InputNumberWidget)