try:
    import simplejson as json
except Exception as e:
    import json
from django.db import models
from django.apps import apps as django_apps
from django.db.models.query import QuerySet



class ListField(models.TextField):

    description = "列表的模型，用,隔开"
 
    def __init__(self, verbose_name=None, modelx=None, **kwargs):
        kwargs['auto_created'] = True
        if modelx and isinstance(modelx, str):
            self.modelx = django_apps.get_model(modelx, require_ready=False)
        else:
            #如果直接是模型
            self.modelx = modelx
        super().__init__(verbose_name, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs


    def get_internal_type(self):
        return "CharField"


    def to_python(self, value):
        if value is None:
            return []
        if len(value) == 0:
            return []
        if isinstance(value, QuerySet):
            return list(value)
         
        value = json.loads(value)
        result = []
        for rid in value:
            if isinstance(rid, dict):
                fileds = [f.name for f in self.modelx._meta.get_fields()]
                if rid.get('id'):
                    x = self.modelx.objects.get(id=rid.get('id'))
                    for key, v in rid.items():
                        if key in fileds:
                            setattr(x, key, v)
                    x.save()
                    result.append(x)
                else:
                    tmp = {}
                    for key, v in rid.items():
                        if key in fileds:
                            tmp[key] = v
                    x = self.modelx(**tmp)
                    x.save()
                    result.append(x)
            else:
                result.append(self.modelx.objects.get(id=rid))
        
        return result

        
    def from_db_value(self, value, expression, connection, context):
        if not value:
            return []
        if len(value) == 0:
            return []
        if value == '{}':
            return []
        if not isinstance(value, list):
            value = value.split(',')
     
        result = []
        for rid in value:
            result.append(self.modelx.objects.get(id=rid))
        return result
 

    def db_type(self, connection):
        return 'text'

    def rel_db_type(self, connection):
        return 'text'

    def get_db_prep_value(self, value, connection, prepared=False):
       
        if value and isinstance(value, list):
            value = ','.join([str(i.id) for i in value])
        return value


 

    
 
