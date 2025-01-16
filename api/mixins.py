from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet


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


class SerializerByActionMixin:
    serializer_classes = {}

    def get_serializer_class(self):
        serializer_class = self.serializer_classes.get(self.action, self.serializer_class)

        if self.action in ['partial_update', 'update_partial']:
            serializer_class = self.serializer_classes.get('update', self.serializer_class)

        assert serializer_class is not None, f'There is no serializer for "{self.action}" action.'

        return serializer_class


class PermissionByActionMixin:
    permission_classes_by_action = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_action.get(self.action, self.permission_classes)

        if self.action in ['partial_update', 'update_partial']:
            permission_classes = self.permission_classes_by_action.get('update', self.permission_classes)

        assert permission_classes is not None, f'There is no permissions for "{self.action}" action.'
        assert type(permission_classes) is list, f'Permissions for "{self.action}" action should ' \
                                                 f'contain list of Permissions.'

        return [permission() for permission in permission_classes]


class ProModelViewSet(PermissionByActionMixin, SerializerByActionMixin, ModelViewSet):
    pass
