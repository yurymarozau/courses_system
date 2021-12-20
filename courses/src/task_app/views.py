from django.db.models import Q
from lecture_app.models import Lecture
from rest_framework import permissions, serializers, viewsets
from task_app.models import Task, TaskFile, TaskStatement, TaskStatementFile
from task_app.serializers import (TaskStatementCreateSerializer,
                                  TaskStatementDetailsSerializer,
                                  TaskStatementShortDetailsSerializer,
                                  TaskStatementUpdateSerializer)


class TaskStatementViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new task statement.

    destroy:
        Delete a task statement.
        Only a teacher of course can delete task statement.

    retrieve:
        Get the specified task statement.

    list:
        Get a list of all lecture task statements.

    update:
        Update a task statement.
        Only a teacher of course can update task statement.

    partial_update:
        Update a task statement.
        Only a teacher of course can update task statement.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'destroy': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'retrieve': TaskStatement.objects.filter(
                Q(lecture__course__teachers=self.request.user.id) | Q(lecture__course__students=self.request.user.id)
            ),
            'list': TaskStatement.objects.filter(
                Q(lecture__course__teachers=self.request.user.id) | Q(lecture__course__students=self.request.user.id)
            ).filter(lecture=self.request.data.get('lecture')),
            'update': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'partial_update': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': TaskStatementCreateSerializer,
            'retrieve': TaskStatementDetailsSerializer,
            'list': TaskStatementShortDetailsSerializer,
            'update': TaskStatementUpdateSerializer,
            'partial_update': TaskStatementUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        try:
            Lecture.objects\
                .filter(course__teachers=self.request.user.id)\
                .get(pk=self.request.data.get('lecture'))
            serializer.save(author=self.request.user)
        except Lecture.DoesNotExist:
            raise serializers.ValidationError('You can add task statements only in teaching courses')
