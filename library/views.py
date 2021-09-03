from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
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

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.isAuth()
        self.bookToLend = Book.objects.get(pk=request.POST.get('book_id'))
        if self.isAllowed():
            self.creatNewLend()
        self.loadSession()
        return super(HandleLendOut, self).post(request, *args, **kwargs)

    def isAllowed(self):
        if self.bookToLend.faculty == self.request.user.position.department.faculty:
            if Lend.objects.filter(book=self.bookToLend, user=self.request.user, is_active=True).count() == 0:
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

    def isAuth(self):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('library')


class UserDashboard(LoginRequiredMixin, ListView):
    template_name = 'library/user_dashboard.html'
    context_object_name = 'books'
    login_url = reverse_lazy('account:login')

    def get_queryset(self):
        return Lend.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, object_list=None, **kwargs):
        context = super(UserDashboard, self).get_context_data(object_list=None, **kwargs)
        context['history'] = Lend.objects.filter(user=self.request.user, is_active=False)
        return context


class HandleRenewal(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy('account:login')
    url = reverse_lazy('dashboard')

    def __init__(self, *args, **kwargs):
        super(HandleRenewal, self).__init__(*args, **kwargs)
        self.lend_object = Lend()
        self.status = False

    def post(self, request, *args, **kwargs):
        self.lend_object = self.getLendObject()
        if self.isAllowed():
            self.lend_object.renewal -= 1
            self.lend_object.save()

    def getLendObject(self):
        try:
            return Lend.objects.get(book_id=self.request.POST.get('book_id'), user=self.request.user)
        except Lend.DoesNotExist:
            return HttpResponseRedirect(self.url)

    def isAllowed(self):
        return True if self.lend_object.renewal > 0 else False

    def loadSession(self):
        self.request.session['status'] = self.status


class HandelReturn(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy('account:login')
    url = reverse_lazy('dashboard')

    def __init__(self, *args, **kwargs):
        super(HandelReturn, self).__init__(*args, **kwargs)
        self.lend_object = None
        self.status = False

    def post(self, request, *args, **kwargs):
        self.getLendObject()
        self.lend_object.is_active = False
        self.lend_object.save()
        self.returnQuantityBack()
        self.status = True
        self.loadSession()
        return super(HandelReturn, self).post(request, *args, **kwargs)

    def getLendObject(self):
        try:
            self.lend_object = Lend.objects.get(id=self.request.POST.get('lend_id'))
        except Lend.DoesNotExist:
            print('redirected')
            return HttpResponseRedirect(self.url)

    def loadSession(self):
        self.request.session['status'] = self.status

    def returnQuantityBack(self):
        returned_book = Book.objects.get(id=self.lend_object.book.id)
        returned_book.quantity += 1
        returned_book.save()
