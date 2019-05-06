# -*- coding: utf-8 -*-
import base64

import django
from django.db import models
from django.utils import six

try:
    import cPickle as pickle
except ImportError:
    import pickle


if django.VERSION < (1, 8):
    PickledObjectFieldBase = six.with_metaclass(models.SubfieldBase, models.Field)
else:
    PickledObjectFieldBase = models.Field


class PickledObjectField(PickledObjectFieldBase):
    """
    this version of pickled object does not work for pickling a single string. it must be some object, dict, list...
    """

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, str) and value is not '':
            # If the value is a sting and an error is raised in de-pickling
            # it should be allowed to propogate.
            value = value.encode()  # encode str to bytes
            value = base64.b64decode(value)
            return pickle.loads(value)
        # its already whatever was pickled
        return value

    def get_prep_value(self, value):
        return base64.b64encode(pickle.dumps(value)).decode()

    def get_internal_type(self):
        return 'TextField'
