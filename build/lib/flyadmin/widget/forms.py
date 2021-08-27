try:
    import simplejson as json
except Exception as e:
    import json
import datetime
from uuid import uuid4
from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
 

class StepsNormalWidget(forms.TextInput):
    template_name = 'widget/steps_normal_widget.html'
    
    def __init__(self, attrs={}):
        super(StepsNormalWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        default = self.attrs.get('default', [])
        if value:
            values = value
        else:
            values = [
                        ['root', {'title': '开始', 'color': 'red'}]
                      ]
        return mark_safe(render_to_string(self.template_name, {'name':name, 'value':value, 'values':values, 'defaults':default}))


class StepsWidget(forms.TextInput):
    template_name = 'widget/steps_widget.html'
    
    def __init__(self, attrs={}):
        super(StepsWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        users = self.attrs.get('users', [])
        if value:
            values = value
        else:
            values = [
                        ['root', {'title': '开始', 'color': 'red'}]
                      ]
        return mark_safe(render_to_string(self.template_name, {'name':name, 'value':value, 'values':values, 'users':users}))



class UploadFileWidget(forms.TextInput):
    template_name = 'widget/upload_file_image_widget.html'
    
    def __init__(self, attrs={}):
        super(UploadFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        upload_path = self.attrs.get('upload_path')
        if value:
            values = value
            rows = value.split(',')
            tmp  = []
            for row in rows:
                tmp.append({'name':row.split('/')[-1], 'url':row})
            value = tmp
        else:
            values = ""
            value = []
        return mark_safe(render_to_string(self.template_name, {'name':name, 'value':value, 'upload_path':upload_path, 'values':values}))


class TimelineWidget(forms.TextInput):
    template_name = 'widget/timeline_widget.html'
     
    def __init__(self, attrs={}):
        super(TimelineWidget, self).__init__(attrs)
 
    def render(self, name, value, attrs = None, renderer=None):
        activities = []
        category = self.attrs.get('category', 1)
        colors = {'info':'#909399', 'warning':'#E6A23C', 'success':'#67C23A'}
        x = {1:'info', 3:'success', 4:'warning', 2:'info'}
        if value:
            for v in value:
                head_type = x.get(v.status)
                color = colors.get(head_type)
                if category == 1:
                    activities.append({
                                      'content': v.title,
                                      'timestamp': v.create_time.strftime('%Y-%m-%d %H:%M'),
                                      'size': 'large',
                                      'type': head_type,
                                      'color': color,
                                      'icon': 'el-icon-{}'.format(head_type),
                                      'id':v.id,
                                      'user': v.created_by.name
                                    })
                else: 
                    activities.append({
                                      'content': v.description,
                                      'timestamp': v.create_time.strftime('%Y-%m-%d %H:%M'),
                                      'size': 'large',
                                      'type': head_type,
                                      'color': color,
                                      'icon': 'el-icon-{}'.format(head_type),
                                      'user': v.title,
                                      'id':v.id
                                    })

        return mark_safe(render_to_string(self.template_name, {
                                                                'name':name,  
                                                                'value':json.dumps(activities),
                                                                'activities':activities
                                                                }
                                        ))

class CheckboxWidget(forms.TextInput):
    template_name = 'widget/checkbox_widget.html'
    
    def __init__(self, attrs={}):
        super(CheckboxWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        if value:
            values = value.split(',')
        else:
            values = []
            value = ''
        items = self.attrs.get('items', [])
        return mark_safe(render_to_string(self.template_name, {
                                                                'name':name,  
                                                                'value':value,
                                                                'items':items,
                                                                'values':values
                                                                }
                                        ))



class InputNumberWidget(forms.TextInput):
    template_name = 'widget/input_number_widget.html'
    
    def __init__(self, attrs={}):
        super(InputNumberWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        if not value:
            value = 0
        return mark_safe(render_to_string(self.template_name, {
                                                                'name':name,  
                                                                'value':value
                                                                }
                                        ))


class SelectBoxWidget(forms.TextInput):
    template_name = 'widget/select_box_widget.html'
    
    def __init__(self, attrs={}):
        super(SelectBoxWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        tmp = self.attrs.get('companys', [])
        if not value:
            value = ''
        return mark_safe(render_to_string(self.template_name, {
                                                                'name':name,  
                                                                'value':value, 
                                                                'selects':json.dumps(tmp)
                                                                }
                                        ))



class MutilBoxWidget(forms.TextInput):
    template_name = 'widget/multi_box_widget.html'
    
    def __init__(self, attrs={}):
        super(MutilBoxWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        columns, columns_name, path = [], [], ''
        if attrs:
            path = self.attrs.get('path', '')
            columns = self.attrs.get('columns', [])
            columns_name = self.attrs.get('columns_name', [])
        tmp = []
        if value and isinstance(value, list):
            for row in value:
                cols = {'uid':str(uuid4()), 'id':row.id, 'xeditor':0}
                for col in columns:
                    cols[col] = getattr(row, col, '')  
                tmp.append(cols)
        keys = list(zip(columns, columns_name))
        return mark_safe(render_to_string(self.template_name, {'name':name,  'value':value, 'data':json.dumps(tmp), 'columns_name':keys, 'path':path}))



class TagWidget(forms.TextInput):
    template_name = 'widget/tag_widget.html'
    def __init__(self, attrs={}):
        super(TagWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None):
        if not value:
            values = []
        else:
            values = value.split(',')
        return mark_safe(render_to_string(self.template_name, {'name':name, 'value':value, 'values':values}))
  


class DateTimeWidget(forms.DateTimeInput):
    template_name = 'widget/picker_widget.html'

    def __init__(self, attrs={}, format='%Y-%m-%d %H:%M:%S'):
        super(DateTimeWidget, self).__init__(attrs)
    
    def decompress(self, value):
        return [value.date(), value.time()]

    def value_from_datadict(self, data, files, name):
        x = data.get(name, None)
        if x:
            x = datetime.datetime.strptime(x[:19], '%Y-%m-%d %H:%M:%S')
            return [x.date(), x.time()]
        return [None, None]

    def render(self, name, value, attrs = None, renderer=None):
        if not value:
            value = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return mark_safe(render_to_string(self.template_name, {'name':name, 'value':value}))
   
   

class MutiTableWidget(forms.Textarea):
    template_name = 'widget/details_muti_table.html'

    def __init__(self, attrs = {}):
        super(MutiTableWidget, self).__init__(attrs)

    def render(self, name, value, attrs = None, renderer=None, *args, **kwargs):
        columns = self.attrs.get('columns', [])
        if not value:
            value = []
        return mark_safe(render_to_string(self.template_name, {'columns':columns, 'name':name, 'values':value}))
  



class EditorWidget(forms.Textarea):
    class Media:
        js = ('/static/admin/js/vendor/wangEditor.min.js',)
    
    template_name = 'widget/editor_widget.html'

    def __init__(self, attrs = {}):
        super(EditorWidget, self).__init__(attrs)
 
    def render(self, name, value, attrs = None, renderer=None):
        if not value:
            value = ''
        upload_path = self.attrs.get('upload_path')
        return mark_safe(render_to_string(self.template_name, {'name':name, 'value':value, 'upload_path':upload_path}))
  
  


class UploadImagesWidget(forms.TextInput):  
 
    def __init__(self, attrs = {}):  
        super(UploadImagesWidget, self).__init__(attrs)  
  
    def render(self, name, value, attrs = None, renderer=None):
        output = ['<div id="{}_upload">'.format(name)]
        output.append(super(UploadImagesWidget, self).render(name, value, attrs, renderer))  
        output.append('<el-upload')
        output.append('   action="{}" '.format(self.attrs.get('path')))
        output.append('   list-type="picture-card" ')
        output.append('   :on-preview="handlePictureCardPreview"')
        output.append("   :on-success='handleSuccess'")
        output.append('   accept="image/gif, image/jpeg, image/png"')
        output.append('   :file-list="defaults"')
        output.append('   :on-remove="handleRemove">')
        output.append('   <i class="el-icon-plus"></i>')
        output.append('</el-upload>')
        output.append('<el-dialog :visible.sync="dialogVisible">')
        output.append('   <img width="100%" :src="dialogImageUrl" alt="">')
        output.append('</el-dialog></div>')
        output.append('<script type="text/javascript">')
        output.append('   new Vue({')
        output.append('     el: "#{}_upload",'.format(name))
        output.append('     data() {')
        output.append('         return {')
        output.append('                 defaults:{},'.format([{'name':name, 'url':url} for name, url in enumerate(value.split(','))] if value else []))
        output.append('                 files:[],')
        output.append("                 uploads:'{}',".format(','.join(value.split(',') if value else [])))
        output.append("                 dialogImageUrl: '',")
        output.append('                 dialogVisible: false')
        output.append('                }')
        output.append('     },')
        output.append('     methods: {')
        output.append('           handleRemove(file, fileList) {')
        output.append('             var _p = [];')
        output.append('             this.files.forEach(function(item){')
        output.append("                  if(item.lastIndexOf(file['name']) == -1){")
        output.append('                      _p.push(item);')
        output.append('             };')
        output.append('             });')
        output.append('             this.files = _p;')
        output.append("             this.uploads = _p.join(',');")
        output.append('           },')
        output.append('           handlePictureCardPreview(file) {')
        output.append('             this.dialogImageUrl = file.url;')
        output.append('             this.dialogVisible = true;')
        output.append('           },')
        output.append('           handleSuccess(res,file,fileList){')
        output.append('                 if(res.code === 200){')
        output.append('                     this.files.push(res.data.path);')
        output.append("                     this.uploads = this.files.join(',');")
        output.append('                     this.$message({')
        output.append("                        message: '上传成功！',")
        output.append("                        type: 'success'")
        output.append("                     });")
        output.append("                 }else {")
        output.append("                         this.$message({")
        output.append("                         message: res.message,")
        output.append("                         type: 'error'")
        output.append("                      });")
        output.append("                 }")
        output.append("            }")
        output.append("         }") 
        output.append("     })</script>")
        output.append('<style type="text/css">#'+name+'_upload ul{padding-left:0!important;margin-left:0!important;padding-right:0!important}</style>')  
        return mark_safe(''.join(output)) 