from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DetailView, ListView
from .forms import OrganizationForm, InviteForm, OrganizationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

from .models import Organization, UserOrganizationRole
from .serializers import OrganizationListSerializer, OrganizationSerializer
from users.models import CustomUser
from django.shortcuts import get_object_or_404

class InviteToOrganizationAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('invite_code')
        user = request.user
        try:
            org = Organization.objects.get(invite_code=code)
        except Organization.DoesNotExist:
            return Response({'invite_code': ['Неверный код организации.']}, status=400)

        if UserOrganizationRole.objects.filter(user=user, organization=org).exists():
            return Response({'invite_code': ['Вы уже состоите в этой организации.']}, status=400)

        UserOrganizationRole.objects.create(user=user, organization=org, role='employee')
        return Response({'detail': 'Вы успешно вступили в организацию!'})

class MyOrganizationsAPI(APIView): # мои организации
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        org_ids = UserOrganizationRole.objects.filter(user=request.user).values_list('organization_id', flat=True)
        orgs = Organization.objects.filter(id__in=org_ids)
        data = OrganizationListSerializer(orgs, many=True, context={'request': request}).data
        return Response(data)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    lookup_url_kwarg = 'org_slug'

    # def get_queryset(self):
    #     # Для эндпоинта /my/ возвращаем только организации пользователя
    #     if self.action == 'list' and 'my' in self.request.path:
    #         return Organization.objects.filter(
    #             userorganizationrole__user=self.request.user
    #         )
    #     return super().get_queryset()

class OrganizationCreateView(CreateView):
    form_class = OrganizationForm
    template_name = 'organizations/create.html'

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'slug': self.kwargs['slug']})

class OrganizationInviteView(FormView):
    form_class = InviteForm
    template_name = 'organizations/invite.html'

    def form_valid(self, form):
        invite_code = form.cleaned_data['invite_code']
        organization = get_object_or_404(Organization, invite_code=invite_code)

        if UserOrganizationRole.objects.filter(user=user, organization=organization).exists(): # проверяет есть ли уже пользователь в организации
            form.add_error('invite_code', 'Вы уже состоите в этой организации.')
            return self.form_invalid(form)

        self.organization = organization  # сохраняет организацию для использования в get_success_url

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'slug': self.organization.slug})

class OrganizationListView(LoginRequiredMixin, ListView): #
    model = Organization
    template_name = 'organizations/organizations_list.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        user = self.request.user
        organization_ids = UserOrganizationRole.objects.filter(user=user).values_list('organization', flat=True) #
        return Organization.objects.filter(id_in=organization_ids)

    # def get_context_data(self, **kwargs): # не нужно, это для проверки прав на создание
    #     context = super().get_context_data(**kwargs)
    #     context['can_create_organization'] = True  
    #     return context

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'organizations/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'org_slug'
    context_object_name = 'organization'

class OrganizationSettingsView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organizations/settings.html'
    slug_field = 'slug'
    slug_url_kwarg = 'org_slug'

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'slug': self.object.slug})