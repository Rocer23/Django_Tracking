from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Comments


class OwnershipRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        comment_id = kwargs.get("comment_id")
        task_id = kwargs.get("task_id")

        comment = get_object_or_404(Comments, id=comment_id, task_id=task_id)

        if request.user != comment.user:
            return JsonResponse({'error': "You are not allowed to modify this comment"}, status=403)

        self.comment = comment
        return super().dispatch(request, *args, **kwargs)