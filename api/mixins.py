from rest_framework.generics import GenericAPIView


class SerializerByMethodMixin:
    serializer_classes = {}

    def get_serializer_class(self):
        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class PermissionByMethodMixin:
    permission_classes_by_method = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_method.get(self.request.method)

        assert permission_classes is not None, f'There is no permissions for "{self.request.method}" method.'
        assert type(permission_classes) is list, f'Permissions for "{self.request.method}" method should ' \
                                                     f'contain list of Permissions.'

        return [permission() for permission in permission_classes]


class ProGenericAPIView(SerializerByMethodMixin, PermissionByMethodMixin, GenericAPIView):
    pass

