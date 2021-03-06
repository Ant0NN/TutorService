# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from BaseApp.models import CustomUser, Tutor, Pupil, Additional_information, Mail, Messages, Views, TypeSubject, Subject, Rating, Reviews
import datetime
import re
from math import ceil
from django.views.generic import ListView, View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin
from BaseApp.forms import Log_in, Registration, Tutor_settings_form, Additional_inf_settings_form, Additions_form, Custom_user_form, Contact_form, Rating_form, CommentForm
from django.utils.decorators import method_decorator
from BaseApp.decorators import no_login_please, check_add_subject__for_tutor, check_questionnaire__for_tutor
from django.core.exceptions import ObjectDoesNotExist


class homepage(ListView, TemplateResponseMixin, FormMixin):
    template_name = "BaseApp/login.html"
    success_url = reverse_lazy("tutor_service:homepage")
    queryset = CustomUser
    context_object_name = 'custom_user'
    paginate_by = 5
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(homepage, self).get_context_data(**kwargs)
        context["contact_form"] = Contact_form()
        context["type_subject"] = TypeSubject.objects.all()
        count = Tutor.objects.count()
        p = []
        for page in range(int(ceil(count*1.0/self.paginate_by))):
            p.append(page + 1)
        context["count"] = p

        if self.request.user.is_authenticated():
            context["email"] = CustomUser.objects.get(id=self.request.user.id)
            u = Tutor.objects.filter(username=self.request.user.id)
            if not u:
                context["is_authenticated"] = True
                context["is_tutor"] = False
            else:
                context["is_tutor"] = True
        return context

    def get_queryset(self, **kwargs):
        list=[]
        try:
            for tutor in Tutor.objects.filter():
                list.append(self.queryset.objects.get(username=tutor.username))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("tutor_service:homepage"))
        return list

    def get(self, request, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

class letter_list(homepage):
    template_name = 'BaseApp/mail.html'
    context_object_name = 'email'
    model = CustomUser

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(letter_list, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(letter_list, self).get_context_data(**kwargs)
        context["email"] = CustomUser.objects.get(id=self.request.user.id)
        return context

class LoginView(homepage):

    form_class = Log_in

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["f"] = self.get_form(self.get_form_class())
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.success_url)
            else:
                return HttpResponseRedirect(reverse('tutor_service:login'))
        else:
            return HttpResponseRedirect(reverse('tutor_service:login'))

    def form_invalid(self, form):
        return self.get(self.request)

def categories(request):
    type_subject = TypeSubject.objects.all()
    return render(request, 'BaseApp/categories.html', {"type_subject": type_subject, })


def sort(request, subj_name):
    custom_user = []
    for x in Additional_information.objects.filter(subject_name=subj_name):
        custom_user.append(CustomUser.objects.get(username=x.tutor))
    p = []
    for page in range(int(ceil(Tutor.objects.count()*1.0/5))):
        p.append(page + 1)
    is_authenticated = False
    contact_form = Contact_form()
    if request.user.is_authenticated():
        u = Tutor.objects.filter(username=request.user.id)
        if not u:
            is_authenticated = True
    d = True
    if len(custom_user):
        d = False

    return render(request, 'BaseApp/login.html', {"custom_user": custom_user, "count": p, "is_authenticated": is_authenticated, "contact_form ": contact_form, "d": d})




def info(request, id):
    c = CustomUser.objects.get(id=id)
    t = Tutor.objects.get(username=c)
    r = Rating.objects.get(tutor_name=t)
    comment = CommentForm()
    rating = Rating_form()
    is_authenticated = False
    contact_form = Contact_form()
    if request.user.is_authenticated():
        u = Tutor.objects.filter(username=request.user.id)
        if not u:
            is_authenticated = True

    if request.method == "POST":
        comment = CommentForm(request.POST)
        rr = Rating_form(request.POST)
        if comment.is_valid() and rr.is_valid():
            q = Reviews()
            q.tutor = t
            q.review = comment.cleaned_data["comment_text"]
            q.pupil = Pupil.objects.get(username=CustomUser.objects.get(id=request.user.id))
            d = Rating.objects.get(tutor_name=t)
            d.count += 1
            d.rating = round((d.rating*(d.count-1)+float(rr.cleaned_data["rating"]))/d.count, 3)
            d.tutor_name = t
            q.rating = rr.cleaned_data["rating"]
            q.save()
            d.save()
            comment = CommentForm()
            r = Rating.objects.get(tutor_name=t)
            return render(request, 'BaseApp/info.html',
                  {'Tutor': t, 'custom_user': c, 'r': r, "comment": comment, "rating": rating, "id": id, "is_authenticated": is_authenticated, "contact_form": contact_form})
    return render(request, 'BaseApp/info.html',
                  {'Tutor': t, 'custom_user': c, 'r': r, "comment": comment, "rating": rating, "id": id, "is_authenticated" : is_authenticated, "contact_form": contact_form})


class mail(homepage):
    form_class = Contact_form

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(mail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return HttpResponseRedirect(reverse('tutor_service:homepage'))

    def get_context_data(self, request, **kwargs):
        context = super(mail, self).get_context_data(request, **kwargs)
        context['error_message'] = request.GET['error_message']
        return context

    def post(self, request, *args, **kwargs):
        contact_form = self.get_form(self.get_form_class())
        to_email = request.POST["to_email"]
        if contact_form.is_valid():
            return self.form_valid(contact_form, to_email)
        else:
            return self.form_invalid(contact_form, to_email)

    def form_valid(self, contact_form, to_email):
        first_name = contact_form.cleaned_data["first_name"]
        last_name = contact_form.cleaned_data["last_name"]
        category = contact_form.cleaned_data["category"]
        number_telephone = contact_form.cleaned_data["number_telephone"]

        if validator_number_telephone(number_telephone):
            mail = Mail()
            custom_user = CustomUser.objects.get(email=to_email)
            mail.user = custom_user
            mail.from_email = self.request.user.email
            mail.from_user = self.request.user
            mail.date = datetime.datetime.now()
            mail.save()

            messages = Messages()
            messages.subject = mail
            message = u'Здравствуйте , я '+last_name +' '+ first_name+','+category+u', '+u'хотел бы записаться к вам на репетиторство'+u'. Мои контактные данные: '+number_telephone
            messages.message = message
            messages.save()

            return HttpResponseRedirect(reverse('tutor_service:homepage'))
        else:
            return HttpResponseRedirect(reverse('tutor_service:homepage'))

    def form_invalid(self, contact_form, to_email):
        return HttpResponseRedirect(reverse('tutor_service:homepage'))

def validator_number_telephone(number_telephone):
    p = re.compile('([0-9]{1,3}\s\([0-9]{2,8}\)\s[0-9]{1,6}\-[0-9]{1,6}\-[0-9]{1,6})|(\+[0-9]{1,3}\-[0-9]{2,8}\-[0-9]{1,6}\-[0-9]{1,6}\-[0-9]{1,6})|([0-9]{1,3}[0-9]{2,8}[0-9]{1,6}[0-9]{1,6}[0-9]{1,6})')
    m = p.match(number_telephone)
    if m:
        return True
    else:
        return False

class views(homepage):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(views, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return HttpResponseRedirect(reverse('tutor_service:homepage'))

    def post(self, request, *args, **kwargs):
        confirm_or_denial = request.POST["click"]
        to_email = request.POST["to_email"]
        m = Mail()
        mes = Messages()
        custom_user = CustomUser.objects.get(email=to_email)
        if confirm_or_denial == 'denial':
            with transaction.commit_on_success():
                m.user = custom_user
                m.from_email = request.user.email
                m.from_user = request.user
                m.date = datetime.datetime.now()
                m.save()

                mes.subject = m
                mes.message = u'Заявка отклонена'
                mes.save()

                #delete later

                m = Mail.objects.filter(Q(user=request.user), Q(from_email=to_email))
                m.delete()
        else:
            tutor = Tutor.objects.get(username=request.user)
            pupil = Pupil.objects.get(username=custom_user)
            view = Views()

            view.tutor = tutor
            view.pupil = pupil
            view.date = datetime.datetime.now()
            view.save()

            m.user = custom_user
            m.from_email = request.user.email
            m.from_user = request.user
            m.date = datetime.datetime.now()
            m.save()

            mes.subject = m
            mes.message = u'Заявка принята'
            mes.save()

            #delete later

            m = Mail.objects.filter(Q(user=request.user), Q(from_email=to_email))
            m.delete()

        return HttpResponseRedirect(reverse('tutor_service:homepage'))

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('tutor_service:login'))


@no_login_please
def registration(request):
    if request.user.is_anonymous():
        if request.POST:

            r = Registration(request.POST)

            tutor_form = Tutor_settings_form(request.POST, request.FILES)

            add_form = Additional_inf_settings_form(request.POST)

            if r.is_valid():
                username = request.POST["username"]
                password = request.POST["password"]
                password2 = request.POST["confirm_password"]
                email = request.POST["email"]
                city = request.POST["city"]
                category = request.POST["category"]
                address = request.POST["address"]

                u = CustomUser.objects.filter(username=username)

                if u:
                    return render(request, 'BaseApp/registration.html',
                                  {"error_message": "Аккаунт уже существует, введите другой логин ", 'reg_form': r,
                                   'tutor_form': tutor_form, 'add_form': add_form})

                u = CustomUser.objects.filter(email=email)

                if u:
                    return render(request, 'BaseApp/registration.html',
                                  {"error_message": "Такой почтовый адрес уже существует, введите другой",
                                   'reg_form': r, 'tutor_form': tutor_form, 'add_form': add_form})

                if validator_password(password) == True:
                    if (password != password2):
                        return render(request, 'BaseApp/registration.html',
                                      {"error_message": "Пароли не совпадают", 'reg_form': r, 'tutor_form': tutor_form,
                                       'add_form': add_form})
                else:
                    return render(request, 'BaseApp/registration.html',
                                  {"error_message": "Некорректный пароль", 'reg_form': r, 'tutor_form': tutor_form,
                                   'add_form': add_form})

                if validator_city(city) == False:
                    return render(request, 'BaseApp/registration.html',
                                  {
                                      "error_message": "Пожалуйста, введите корректное название своего города или выберете из списка",
                                      'reg_form': r, 'tutor_form': tutor_form, 'add_form': add_form})

                if int(category) == 1:
                    return render(request, 'BaseApp/registration.html',
                                  {"error_message": "Пожалуйста, выберете категория из списка", 'reg_form': r,
                                   'tutor_form': tutor_form, 'add_form': add_form})
                else:
                    if int(category) == 2:

                        if tutor_form.is_valid() and add_form.is_valid():
                            first_name = request.POST["first_name"]
                            patronymic = request.POST["patronymic"]
                            if check(first_name):
                                if check(patronymic):
                                    u = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                                       City=city, Category=category, address=address,
                                                                       first_name=first_name, patronymic=patronymic)
                                    u.save()

                                    new_tutor = tutor_form.save(commit=False)
                                    new_tutor.username = u
                                    new_tutor.save()

                                    new_add = add_form.save(commit=False)
                                    new_add.tutor = u
                                    new_add.save()
                                    d = Rating()
                                    d.count = 0
                                    d.rating = 0
                                    d.tutor_name = new_tutor
                                    d.save()
                                else:
                                    return render(request, 'BaseApp/registration.html',
                                              {"error_message": "Пожалуйста, корректно введите свои данные", 'reg_form': r,
                                               'tutor_form': tutor_form, 'add_form': add_form})
                            else:
                                return render(request, 'BaseApp/registration.html',
                                          {"error_message": "Пожалуйста, корректно введите свои данные", 'reg_form': r,
                                           'tutor_form': tutor_form, 'add_form': add_form})
                        else:
                            return render(request, 'BaseApp/registration.html',
                                          {"error_message": "Пожалуйста, введите корректные данные", 'reg_form': r,
                                           'tutor_form': tutor_form, 'add_form': add_form})

                    if int(category) == 3:
                        u = CustomUser.objects.create_user(username=username, email=email,
                                                           password=password, City=city,
                                                           Category=category, address=address)
                        u.save()
                        pupil = Pupil()
                        pupil.username = u
                        pupil.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('tutor_service:homepage'))
                    else:
                        return HttpResponseRedirect(reverse('BaseApp:login'))
                else:
                    return HttpResponseRedirect(reverse('BaseApp:login'))
            else:
                return render(request, 'BaseApp/registration.html',
                              {'reg_form': r, 'tutor_form': tutor_form, 'add_form': add_form})
        else:
            r = Registration()
            tutor_form = Tutor_settings_form(instance=Tutor())
            add_form = Additional_inf_settings_form(instance=Additional_information())
            return render(request, 'BaseApp/registration.html',
                          {'reg_form': r, 'tutor_form': tutor_form, 'add_form': add_form})
    else:
        return HttpResponseRedirect(reverse('tutor_service:homepage'))

def check(name):
    p = re.compile(u'^[а-яА-ЯёЁa-zA-Z][а-яА-ЯёЁa-zA-Z]{1,}[а-яА-ЯёЁa-zA-Z]$')
    m = p.match(name)
    if m:
        return True
    else:
        return False

@login_required
@check_questionnaire__for_tutor
def settings_for_questionnaire(request):
    if request.POST:
        custom_user_form = Custom_user_form(request.POST)
        tutor_form = Tutor_settings_form(request.POST, request.FILES)
        tutor_avatar = Tutor.objects.get(username=request.user)
        add_form = Additional_inf_settings_form(request.POST)

        if tutor_form.is_valid() and add_form.is_valid() and custom_user_form.is_valid():


            c = CustomUser.objects.get(id=request.user.id)
            c.first_name = custom_user_form.cleaned_data["first_name"]
            c.patronymic = custom_user_form.cleaned_data["patronymic"]
            c.save()

            t = Tutor.objects.get(username=c)
            t.delete()

            new_tutor = tutor_form.save(commit=False)
            new_tutor.username = c
            new_tutor.save()


            for item in Additional_information.objects.filter(tutor=c):
                item.delete()

            new_add = add_form.save(commit=False)
            new_add.tutor = c
            new_add.save()

            return HttpResponseRedirect(reverse('tutor_service:homepage'))

        else:
            return render(request, 'BaseApp/settings.html',
                              {'tutor_form': tutor_form, 'add_form': add_form, 'user': tutor_avatar})
    else:
        custom_user_form = Custom_user_form(instance=CustomUser.objects.get(id=request.user.id))
        tutor_form = Tutor_settings_form(instance=Tutor.objects.get(username=request.user))
        add_form = []
        for d in Additional_information.objects.filter(tutor=request.user):
            add_form.append(Additional_inf_settings_form(instance=d))
        tutor_avatar = Tutor.objects.get(username=request.user)
        return render(request, 'BaseApp/settings.html',
                      {'custom_user_form': custom_user_form, 'tutor_form': tutor_form, 'add_form': add_form, 'user': tutor_avatar})


class add_subject(ListView, TemplateResponseMixin, FormMixin):
    form_class = Additions_form
    template_name = "BaseApp/addSubject.html"
    model = CustomUser
    context_object_name = "subject_list"

    @method_decorator(login_required)
    @check_add_subject__for_tutor
    def dispatch(self, request, *args, **kwargs):
        return super(add_subject, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(add_subject, self).get_context_data(**kwargs)
        context["add_form"] = self.get_form(self.get_form_class())
        return context

    def get_queryset(self, **kwargs):
        subject_list = self.model.objects.get(id=self.request.user.id)
        return subject_list

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        add_form = self.get_form(self.get_form_class())
        if add_form.is_valid():
            return self.form_valid(add_form)
        else:
            return self.form_invalid(add_form)

    def form_valid(self, add_form, **kwargs):

        subject_name = add_form.cleaned_data["subject_name"]
        section = self.request.POST["section"]
        additions = add_form.cleaned_data["additions"]
        pupil_category = add_form.cleaned_data["pupil_category"]
        price = add_form.cleaned_data["price"]

        add = Additional_information()
        user = CustomUser.objects.get(id=self.request.user.id)
        add.tutor = user
        add.subject_name = subject_name
        add.section = section
        add.additions = additions
        add.pupil_category = pupil_category
        add.price = price
        add.save()

        return HttpResponseRedirect(reverse('tutor_service:add_subject'))

    def form_invalid(self, form):
        return self.get(self.request)


def validator_city(city):
    p = re.compile(u'^[а-яА-ЯёЁa-zA-Z][A-Za-zА-Яа-я\\s\\\(\\\-]{1,30}[A-Za-zА-Яа-я\\\)]$')
    m = p.match(city)
    if m:
        return True
    else:
        return False


def validator_password(password):
    p = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9]{6,28}[a-zA-Z0-9]$')
    m = p.match(password)
    if m:
        return True
    else:
        return False
