import requests

from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from .permissions import IsAuthorOrAllowAny, IsStaff, IsAny
from .serializers import CommentSerializer, PostSerializer, MarkPostSerializer
from .models import Comment, Post, PostMark


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthorOrAllowAny, ]

    def perform_create(self, serializer):
        TOKEN = "6005669510:AAHLKMC3_dELLM6y1S80rPTORXAPuLxMIR0"
        author = self.request.user
        chat_id = author.telegram_chat_id
        message = f'Ваш пост опубликован'
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url).json()
        serializer.save(author=self.request.user)

    @action(methods=['POST', ], detail=True, permission_classes=[permissions.IsAuthenticated, ],
            serializer_class=MarkPostSerializer)
    def mark_post(self, request, pk=None):
        serializer = MarkPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                post_id=pk
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAny, IsStaff, ]

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            anon_user = User.objects.get(username='anonymus')
            serializer.save(author=anon_user)
        else:
            serializer.save(author=self.request.user)





