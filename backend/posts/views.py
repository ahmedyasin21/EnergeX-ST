import json
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer


@api_view(["GET", "POST"])
def posts_list(request):
    if request.method == "GET":
        cached_posts = cache.get("posts")
        if cached_posts:
            return Response(cached_posts, status=status.HTTP_200_OK)

        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        cache.set("posts", serializer.data)  # uses default TIMEOUT from settings
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("posts")  # invalidate cache
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def post_detail(request, pk):
    cache_key = f"post:{pk}"
    cached_post = cache.get(cache_key)

    if cached_post:
        return Response(cached_post, status=status.HTTP_200_OK)

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post)
    cache.set(cache_key, serializer.data)  # uses default TIMEOUT
    return Response(serializer.data, status=status.HTTP_200_OK)
