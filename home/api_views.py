from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer

@api_view(['GET'])
def blog_list_api(request):
    blog = Blog.objects.all().order_by('-created_at')
    serializer = BlogSerializer(blog, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def blog_detail_api(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = BlogSerializer(blog)
    return Response(serializer.data)

@api_view(['PUT'])
def blog_update_api(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog Not found"}, status=404)
    
    serializer = BlogSerializer(blog,data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_create_api(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def blog_delete_api(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Only the author to delete
    if blog.author != request.user:
        return Response({"error": "You do not have permission to delete this blog."}, status=status.HTTP_403_FORBIDDEN)
    
    blog.delete()
    return Response({"message": "Blog deleted successfully."}, status=status.HTTP_200_OK)