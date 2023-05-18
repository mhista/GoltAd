from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.shortcuts import redirect, reverse
from django.contrib import messages

class AdCreatePerm(AccessMixin):
    """Verify that the current user is authenticated and checks if the user has a company."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.has_company or not request.user.is_authenticated:
            messages.info(request, 'Setup a business entity to access Ads page')
            return redirect(reverse('golt:create-company'))
        return super().dispatch(request, *args, **kwargs)

class CompanyAccessPerm(AccessMixin):
    """Verify that the current user is authenticated, and checks ifnthe user has a user profile."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.has_profile or not request.user.is_authenticated:
            messages.info(request, 'complete your profile setup to access the requested page')
            return redirect(reverse('golt:create-profile'))
        return super().dispatch(request, *args, **kwargs)


