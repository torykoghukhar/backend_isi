from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.threads.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ThreadSerializer
        return ThreadSerializer

    def perform_destroy(self, instance):
        if self.request.user not in instance.participants.all():
            raise PermissionError("Access denied.")
        instance.delete()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs.get('thread_pk')
        thread = get_object_or_404(Thread, id=thread_id)
        if self.request.user not in thread.participants.all():
            raise PermissionDenied("You are not a participant of this thread.")
        return Message.objects.filter(thread=thread).order_by('created')

    def perform_create(self, serializer):
        thread_id = self.kwargs.get('thread_pk')
        thread = get_object_or_404(Thread, id=thread_id)

        if self.request.user not in thread.participants.all():
            raise PermissionDenied("You are not a participant of this thread.")

        serializer.save(sender=self.request.user, thread=thread)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, thread_pk=None, pk=None):
        message = self.get_object()
        if request.user not in message.thread.participants.all():
            return Response({'error': 'Access denied.'}, status=403)
        message.is_read = True
        message.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request, thread_pk=None):
        thread = get_object_or_404(Thread, id=thread_pk)
        if request.user not in thread.participants.all():
            return Response({'error': 'Access denied.'}, status=403)
        count = Message.objects.filter(
            thread=thread,
            is_read=False
        ).exclude(sender=request.user).count()
        return Response({'unread_count': count})
