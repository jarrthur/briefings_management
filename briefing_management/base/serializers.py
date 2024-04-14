from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Custom serializer to specify which fields or which fields
    should not be included in the serializer return:
    Ex: serializer = ProducerSerializer(fields=["name", "cnpj"])
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude_fields = kwargs.pop("exclude_fields", None)
        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        elif exclude_fields:
            not_allowed = set(exclude_fields)
            for field_name in not_allowed:
                self.fields.pop(field_name)
