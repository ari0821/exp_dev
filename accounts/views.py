from __future__ import unicode_literals
from django.shortcuts import render
from django import forms
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from .serializer import ExpUserSerializer
from .models import ExpUser, ExpUserManager

class AuthRegister(generics.CreateAPIView):
    pemission_classes = (permissions.AllowAny,)
    queryset = ExpUser.object.all()
    serializer_class = ExpUserSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = ExpUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthInfoGetView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ExpUser.objects.all()
    serializer_class = ExpUserSerializer

    def get(self, request, format=None):
        return Response(data={
            'username': request.user.username,
            'email': request.user.email,
            'profile': request.user.profile,
            },
            status=status.HTTP_200_OK)

class AuthInfoUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExpUserSerializer
    lookup_field = 'email'
    queryset = ExpUser.objects.all()

    def get_object(self):
        try:
            instance = self.queryset.get(email=self.request.user)
            return instance
        except ExpUser.DoesNotExist:
            raise Http404

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tenant_id = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "tenant_id", "password1", "password2")

class UserSignUp(SuccessMessageMixin,CreateView):
    model = User
    form_class = UserSignupForm
    success_url = reverse_lazy('items:index')
    success_message = "User created successfully"
    template_name = "registration/signup.html"
    def form_valid(self, form):
        super(UserSignUp,self).form_valid(form)
        # The form is valid, automatically sign-in the user
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user == None:
            # User not validated for some reason, return standard form_valid() response
            return self.render_to_response(self.get_context_data(form=form))
        else:
            # Log the user in
            login(self.request, user)
            # Redirect to success url
            return HttpResponseRedirect(self.get_success_url())


