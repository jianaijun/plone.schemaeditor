from Products.Five import BrowserView
from zope.container.contained import notifyContainerModified
from zope.event import notify
from plone.schemaeditor.utils import SchemaModifiedEvent, sortedFields
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.schemaeditor.interfaces import IEditableSchema


class ChangeFieldsetView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.field = context.field
        self.schema = context.field.interface

    def change(self, fieldset_index):
        """ AJAX method to change the fieldset of a field
        """
        fieldset_index = int(fieldset_index)
        fieldsets = self.schema.getTaggedValue(FIELDSETS_KEY)
        field_name = self.field.__name__

        # get current fieldset
        fieldset_fields = []
        current_fieldset = None
        for fieldset in fieldsets:
            if field_name in fieldset.fields:
                current_fieldset = fieldset

            fieldset_fields.extend(fieldset.fields)

        # get future fieldset
        if len(sortedFields(self.schema)) != len(fieldset_fields):
            # we have a default fieldset
            fieldset_index -= 1

        if fieldset_index >= 0:
            # the field has not been moved into default
            next_fieldset = fieldsets[fieldset_index]
        else:
            next_fieldset = None

        # computing new Position, which is the last position of the new fieldset
        ordered_field_ids = [name for (name, field) in sortedFields(self.schema)]
        if next_fieldset is None:
            # if this is the default,
            new_position = ordered_field_ids.index(fieldset_fields[0])
        else:
            # first we get the first of the fieldsets after the new one
            new_position = None
            for fieldset in fieldsets[fieldsets.index(next_fieldset)+1:]:
                if len(fieldset.fields) > 0:
                    new_position = ordered_field_ids.index(fieldset.fields[0]) - 1
                    break
            else:
                new_position = len(ordered_field_ids) - 1

        schema = IEditableSchema(self.schema)
        schema.moveField(field_name, new_position)

        # move field
        if next_fieldset is not None:
            next_fieldset.fields.append(field_name)

        if current_fieldset is not None:
            current_fieldset.fields.remove(field_name)

        notifyContainerModified(self.schema)
        notify(SchemaModifiedEvent(self.aq_parent.aq_parent))
