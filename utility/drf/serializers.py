

class CreateForRelatedMixin:

    def create_for_related(self, obj_field, obj, serializer_class, data):
        objs = []
        for datum in data:
            serializer = serializer_class(data=datum, context=self.context)
            serializer.is_valid(raise_exception=True)
            objs.append(serializer.save(**{obj_field: obj}))
        return objs
