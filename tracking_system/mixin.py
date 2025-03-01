from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Comments


class CommentOwnershipMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, pk=self.kwargs['pk'])
        if comment.user != request.user:
            return JsonResponse({'error': "Ви не можете змінювати цей коментар"}, status=403)
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(CommentOwnershipMixin, DeleteView):
    model = Comments
    success_url = reverse_lazy('task-detail')
