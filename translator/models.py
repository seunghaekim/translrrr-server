from django.db import models
from app import dbutils


class ContentsHash(models.Model):
    seq = dbutils.default_id(models)
    contents_hash = models.CharField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    updatetime = dbutils.default_updatetime(models)
    createtime = dbutils.default_createtime(models)


class ContentsCache(models.Model):
    seq = dbutils.default_id(models)
    contents_hash = models.ForeignKey(ContentsHash, models.CASCADE)
    translated_text = models.TextField(null=False, blank=False)
    vendor = models.CharField(max_length=16, blank=False, null=False)
    source = models.CharField(max_length=8, blank=False, null=False)
    target = models.CharField(max_length=8, blank=False, null=False)
    createtime = dbutils.default_createtime(models)

    def to_dict(self):
        return {
            'translated_text': self.translated_text,
            'result': True,
            'message': '',
            'cached': self.createtime
        }
