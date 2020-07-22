from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute
from datetime import datetime
import json
import os
import time


class BaseModel(Model):
    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self):
        ret_dict = {}
        for name, attr in self.attribute_values.items():
            ret_dict[name] = self._attr2obj(attr)

        return ret_dict

    def _attr2obj(self, attr):
        if isinstance(attr, list):
            _list = []
            for l in attr:
                _list.append(self._attr2obj(l))
            return _list
        elif isinstance(attr, MapAttribute):
            _dict = {}
            for k, v in attr.attribute_values.items():
                _dict[k] = self._attr2obj(v)
            return _dict
        elif isinstance(attr, datetime):
            return attr.isoformat()
        else:
            return attr


class HitsModel(BaseModel):
    class Meta:
        table_name = os.environ["HITS_TABLE"]
        region = os.environ['REGION']

    sid = UnicodeAttribute(hash_key=True)
    event_id = UnicodeAttribute(range_key=True)
    path = UnicodeAttribute(null=False)
    hostname = UnicodeAttribute(null=False)
    referrer = UnicodeAttribute(null=False)
    resolution = UnicodeAttribute(null=False)
    timezone = UnicodeAttribute(null=False)
    referrer_param = UnicodeAttribute(null=False)
    new_visit = UnicodeAttribute(null=False)
    created = UnicodeAttribute(null=False)


def create_hit_entry(**kwargs):
    hits_model = HitsModel()
    hits_model.sid = kwargs.get("sid")
    hits_model.event_id = kwargs.get("event_id")
    hits_model.path = kwargs.get("path")
    hits_model.hostname = kwargs.get("hostname")
    hits_model.referrer = kwargs.get("referrer")
    hits_model.resolution = kwargs.get("resolution")
    hits_model.timezone = kwargs.get("timezone")
    hits_model.referrer_param = kwargs.get("referrer_param")
    hits_model.new_visit = kwargs.get("new_visit")
    hits_model.created = str(int(time.time()))
    hits_model.save()
    return hits_model
