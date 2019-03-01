# Generate CSV files for models
from django.utils.encoding import smart_str, smart_unicode
from django.db.models.fields.related import ManyToManyField
import re
import csv
from csv import Dialect, register_dialect, QUOTE_MINIMAL
from django.db.models.loading import get_model, get_apps, get_models
from django.db.models import BooleanField
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.defaultfilters import yesno

__all__ = ( 'export', )

class OneofiveDialect(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL
register_dialect("oneofive", OneofiveDialect)


def _field_extractor_function(field):
    """Return a function that extracts a given field from an instance of a model."""
    if field.choices:
        try:
            return (lambda o: smart_unicode(getattr(o, 'get_%s_display' % field.name)()))
        except:
            return ""
    elif isinstance(field, BooleanField):
        return (lambda o: yesno(getattr(o, field.name), "Yes,No"))
    else:
        return (lambda o: smart_unicode(getattr(o, field.name)))

@staff_member_required
def export(request, app_label, model_name):
    """Return a CSV file for this table."""

    # Get the fields of the table
    model = get_model(app_label, model_name)
    if not model:
        raise Http404
    fields = model._meta.fields
    field_funcs = [ _field_extractor_function(f) for f in fields ]

    # set the HttpResponse
    response = HttpResponse(mimetype='text/csv;charset=ISO-8859-1')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.csv' % (app_label, model_name)
    writer = UnicodeWriter(response, quoting=csv.QUOTE_ALL, encoding='iso8859-1', illegal_char_replacement='?')
    
    # Add ManyToMany fields to header
    mtm_declared_fields = getattr(model, 'CsvExport', False) and model.CsvExport().many_to_many_fields or []
    mtm_fields = filter(lambda f: f.name in mtm_declared_fields, model._meta.many_to_many)
    
    # Write the header of the CSV file
    writer.writerow([ f.verbose_name for f in fields ] + [f.verbose_name for f in mtm_fields])
    
    # Do some simple query string check for filters
    filters = {}
    for param_name, param_value in request.REQUEST.items():
        if re.match(r'.+__(exact|lte|gte|year|month)', param_name):
            filters[str(param_name)] = param_value
    #print filters
    # Write all rows of the CSV file
    model_objects = model.objects.all().filter(**filters)
    import pprint
    #pprint.pprint(model_objects)
    for o in model_objects:
        try:
            row = [ func(o) for func in field_funcs ] + ["", "", ""]
            # ManyToMany field support
            row += [[ smart_unicode(fv) for fv in getattr(o, om.name).all()] for om in mtm_fields]
            writer.writerow(row)
        except Exception, e:
            raise DatabaseInconsistency,"there was an error at object %s (%s)" % ( o.id, e )
    # All done
    return response

class UnicodeWriter:
    def __init__(self, f, encoding="utf-8", illegal_char_replacement=None,  **kwds):
        quoting = kwds.pop('quoting', csv.QUOTE_ALL)
        dialect = kwds.pop('dialect', OneofiveDialect)
        self.writer = csv.writer(f, quoting=quoting, dialect=dialect, **kwds)
        self.encoding = encoding
        self.illegal_char_replacement = illegal_char_replacement

    def writerow(self, row):
        #try:
        out_row = []
        for field_string_in in row:
            field_string_out = []
            for field_chr in field_string_in:
                try:
                    field_string_out.append( field_chr.encode(self.encoding) )
                except Exception, e:
                    # a char that cannot be encoded with this encoding
                    if self.illegal_char_replacement==None:
                        raise e
                    else:
                        field_string_out.append(self.illegal_char_replacement)
            out_row.append( ''.join(field_string_out) )
        self.writer.writerow(out_row)
        #self.writer.writerow([s.encode(self.encoding) for s in row])
        #except:
        #    self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

            
class DatabaseInconsistency(Exception):
    "Database Inconsistency"
    pass

# The URL for the spreadsheet
#
# urlpatterns += patterns('foo.utils.spreadsheets',
#     (r"^spreadsheets/(?P<app_label>\w+)/(?P<model_name>\w+)/$", "spreadsheet"), # Return a CSV file for this model
# )