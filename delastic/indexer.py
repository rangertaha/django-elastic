# -*- coding:utf-8 -*-
"""

"""
import re
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import String, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Mapping, Field, Integer, Long, Search
from django.db.models import CharField, TextField, DateField, DateTimeField

from .signals import post_index, pre_index, post_delete, pre_delete
from .settings import DJANGO_ELASTIC

INDEX = DJANGO_ELASTIC.get('index')
HOSTS = DJANGO_ELASTIC.get('hosts')
PORT = DJANGO_ELASTIC.get('port')

DSL_TO_DJANGO_FIELDS = {
    String: [CharField, TextField],
    Date: [DateField, DateTimeField],
    Integer: [],
    Long: [],
    Boolean: [],
}


class IndexMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['_meta'] = IndexOptions(name, bases, attrs)
        return super(IndexMeta, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            # Add cls to the registry
            if cls._meta.model:
                cls.registry[cls._meta.model] = cls

            # Create and add mapping to the registry
            mapping, created = cls._get_mapping(cls._meta.doc_type)
            cls.registry[cls._meta.doc_type] = mapping

            if created and cls._meta.model:
                # Build the mapping from the django model
                cls._update_mapping_from_model(cls._meta.model)

                # Update the mapping from the indexer model
                cls._update_mapping_from_indexer()

            cls.fields = cls._mapping_fields()

        super(IndexMeta, cls).__init__(name, bases, dct)

    def _update_mapping_from_model(cls, model):
        mapping = cls.registry.get(cls._meta.doc_type, None)
        for field in model._meta.get_fields():
            name, value = cls._translate_field(field)
            if name and value and mapping:
                mapping.field(name, value())
        cls.registry[cls._meta.doc_type] = mapping

    def _update_mapping_from_indexer(cls):
        mapping = cls.registry.get(cls._meta.doc_type, None)
        fields = cls._mapping_fields().keys()
        for field in fields:
            cls_field = getattr(cls, field, None)
            if cls_field:
                mapping.field(field, cls_field)
        cls.registry[cls._meta.doc_type] = mapping

    def _get_mapping(cls, doc_type):
        """Gets or creates a mapping object"""
        mapping = cls.registry.get(doc_type, None)
        if isinstance(mapping, Mapping):
            return mapping, False
        return Mapping(doc_type), True

    def _translate_field(cls, field):
        for key, values in DSL_TO_DJANGO_FIELDS.iteritems():
            if type(field) in values:
                return field.name, key
        return None, None

    def _mapping_fields(cls):
        mapping = cls.registry.get(cls._meta.doc_type, {})
        map_dict = mapping.to_dict()
        properties = map_dict.get(
            cls._meta.doc_type, {}).get('properties', {})
        return properties

    def indexer_for_instance(cls, instance):
        indexer = cls.registry.get(instance.__class__, None)
        if callable(indexer):
            return indexer(instance)
        return

    def indexer_for_model(cls, model):
        return cls.registry.get(model, None)

    def init(cls):
        mapping = cls.registry.get(cls._meta.doc_type, None)
        if mapping:
            mapping.save(cls._meta.index, using=cls._meta.es)


class IndexOptions(object):
    def __init__(self, name, bases, attrs):
        meta = attrs.pop('Meta', None)

        self.model = getattr(meta, 'model', None)
        self.fields = getattr(meta, 'fields', [])
        self.exclude = getattr(meta, 'exclude', [])

        # Client Elasticsearch instance
        self.es = getattr(meta, 'client', Elasticsearch(hosts=HOSTS))
        self.index = getattr(meta, 'index', INDEX)

        # Get doc_type name, defaults to lower case class name
        self.doc_type = getattr(
            meta, 'doc_type', re.sub(r'(.)([A-Z])', r'\1_\2', name).lower())


class BaseModelIndex(object):
    def __init__(self, instance=None):
        self.record = {}
        self.instance = instance
        if self.instance:
            self._clean()

    def _clean(self):
        fields = self.fields.keys()
        for field in fields:
            attrname = 'clean_{0}'.format(field)
            clean_func = getattr(self, attrname, None)
            if callable(clean_func):
                attrvalue = clean_func()
                if self._valid(attrvalue, field):
                    self.record[field] = attrvalue
                    #print 'Cleaned: ', field, ': ', attrvalue
                else:
                    # raise error, function is not return correct value
                    pass
            else:
                instance_field = getattr(self.instance, field, None)
                if self._valid(instance_field, field):
                    self.record[field] = instance_field
                else:
                    # Error field value does not match the mapping value type
                    pass

    def clean_id(self):
        if self.instance:
            from django.contrib.contenttypes.models import ContentType
            self.content_type = ContentType.objects.get_for_model(
                self.instance)
            self.django_id = str(self.instance.pk)
        return self.instance.pk

    def timestamp(self):
        return datetime.now()

    def _valid(self, attrname, field):
        # Validate the field via mapping
        return True

    def save(self):
        pre_index.send(sender=self, instance=self.instance)

        body = self.record
        body['timestamp'] = self.timestamp()
        self._meta.es.index(
            index=self._meta.index,
            doc_type=self._meta.doc_type,
            id=self.clean_id(),
            body=body,
        )

        post_index.send(sender=self, instance=self.instance)

    def delete(self):
        pre_delete.send(sender=self, instance=self.instance)

        try:
            self._meta.es.delete(
                index=self._meta.index,
                doc_type=self._meta.doc_type,
                id=self.clean_id(),
            )
        except:
            pass

        post_delete.send(sender=self, instance=self.instance)

    @classmethod
    def search(self, es=None, index=None):
        return Search(
            using=es or self._meta.es,
            index=index or self._meta.index,
            doc_type=self._meta.doc_type,
        )


class ModelIndex(BaseModelIndex, object):
    __metaclass__ = IndexMeta



