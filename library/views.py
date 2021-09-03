from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.base import TemplateView, RedirectView, View

from library.models import Book, Lend
from university_controller import settings


class BookList(LoginRequiredMixin, ListView):
    paginate_by = 10
    login_url = reverse_lazy('account:login')
    template_name = 'library/index.html'
    context_object_name = 'books'
    status = None
    book_lent = None

    def get_queryset(self):
        return Book.objects.filter(faculty=self.request.user.position.department.faculty)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(BookList, self).get_context_data(*args, object_list=None, **kwargs)
        if 'status' in self.request.session and 'book_lent' in self.request.session:
            context['status'] = self.request.session['status']
            context['book_lent'] = Book.objects.get(id=self.request.session['book_lent']).name
            self.flushLentDataSession()
        return context

    def flushLentDataSession(self):
        del self.request.session['status']
        del self.request.session['book_lent']


class HandleLendOut(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy('account:login')
    url = reverse_lazy('library')

    def __init__(self, *args, **kwargs):
        super(HandleLendOut, self).__init__(*args, **kwargs)
        self.bookToLend = Book()
        self.status = False

    def get(self, request, *args, **kwargs):
        self.isAuth()
        self.bookToLend = Book.objects.get(pk=kwargs['book_id'])
        if self.isAllowed():
            self.creatNewLend()
        self.loadSession()
        return super(HandleLendOut, self).get(request, *args, **kwargs)

    def isAllowed(self):
        if self.bookToLend.faculty == self.request.user.position.department.faculty:
            if Lend.objects.filter(book=self.bookToLend, user=self.request.user).count() == 0:
                if self.bookToLend.reminded >= 1:
                    if Lend.objects.filter(user=self.request.user, is_active=True).count() <= settings.MAX_LENT:
                        return True
        return False

    def creatNewLend(self):
        new_lend_data = Lend(user=self.request.user, book=self.bookToLend)
        new_lend_data.save()
        self.status = True

    def loadSession(self):
        self.request.session['status'] = self.status
        self.request.session['book_lent'] = self.bookToLend.id

    def get_queryset(self):
        return

    def isAuth(self):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('library')


class UserDashboard(LoginRequiredMixin, ListView):
    template_name = 'library/user_dashboard.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Lend.objects.filter(user=self.request.user, is_active=True)
