from rest_framework import serializers

from helpers.models import GeneralInfo

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if 'fields' in self.context:
            fields = self.context['fields']
            if fields:
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class GeneralInfoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = GeneralInfo
        fields = "__all__"