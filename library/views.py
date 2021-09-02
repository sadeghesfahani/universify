from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView, RedirectView, View

from library.models import Book, Lend


class BookList(LoginRequiredMixin, ListView):
    paginate_by = 10
    login_url = reverse_lazy('account:login')
    template_name = 'library/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(faculty=self.request.user.position.department.faculty)


class HandleLendOut(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('account:login')
    template_name = 'library/index.html'
    context_object_name = 'books'

    def __init__(self,*args, **kwargs):
        super(HandleLendOut, self).__init__(*args, **kwargs)
        self.bookToLend = str()
        self.status = False

    def setup(self, *args, **kwargs):
        super(HandleLendOut, self).setup(*args, **kwargs)
        self.bookToLend = Book.objects.get(pk=kwargs['book_id'])

    def dispatch(self, request, *args, **kwargs):
        if self.isAllowed():
            self.creatNewLend()
        return super(HandleLendOut, self).dispatch(request, *args, **kwargs)

    def isAllowed(self):
        return True if self.bookToLend.faculty == self.request.user.position.department.faculty else False

    def creatNewLend(self):
        new_lend_data = Lend(user=self.request.user, book=self.bookToLend)
        new_lend_data.save()
        self.status = True

    def get_context_data(self, **kwargs):
        context = super(HandleLendOut, self).get_context_data(**kwargs)
        context['status'] = self.status
        context['lent_book'] = self.bookToLend.id

    def get_queryset(self):
        return Book.objects.filter(faculty=self.request.user.position.department.faculty)
