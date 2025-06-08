from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.threads.all()

    def create(self, request, *args, **kwargs):
        user_ids = request.data.get("participant_ids", [])

        if not isinstance(user_ids, list) or not all(isinstance(uid, int) for uid in user_ids):
            return Response({'error': 'participant_ids must be a list of user IDs.'}, status=400)

        user_ids.append(request.user.id)
        user_ids = list(set(user_ids))

        if len(user_ids) != 2:
            return Response({'error': 'Thread must contain exactly 2 unique participants.'}, status=400)

        existing_threads = Thread.objects.filter(participants__id=user_ids[0])\
                                         .filter(participants__id=user_ids[1])
        for thread in existing_threads:
            if set(thread.participants.values_list("id", flat=True)) == set(user_ids):
                serializer = self.get_serializer(thread)
                return Response(serializer.data)

        thread = Thread.objects.create()
        thread.participants.set(user_ids)
        serializer = self.get_serializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        thread = self.get_object()
        if request.user not in thread.participants.all():
            return Response({'error': 'Access denied.'}, status=403)
        return super().destroy(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs.get('thread_pk')

        thread = get_object_or_404(Thread, id=thread_id)
        if self.request.user not in thread.participants.all():
            return Message.objects.none()
        return Message.objects.filter(thread=thread).order_by('created')

    def perform_create(self, serializer):
        thread_id = self.kwargs.get('thread_pk')
        thread = get_object_or_404(Thread, id=thread_id)

        if self.request.user not in thread.participants.all():
            raise PermissionError("You cannot post messages to this thread.")

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
        try:
            thread = Thread.objects.get(id=thread_pk)
        except Thread.DoesNotExist:
            return Response({'error': 'Thread does not exist.'}, status=404)

        if request.user not in thread.participants.all():
            return Response({'error': 'Access denied.'}, status=403)

        count = Message.objects.filter(
            thread=thread,
            is_read=False
        ).exclude(sender=request.user).count()

        return Response({'unread_count': count})
