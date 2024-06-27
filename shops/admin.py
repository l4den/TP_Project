from django.contrib import admin
from .models import Shop
from workingtimes.models import WorkingTime
from workingtimes.forms import WorkingTimeForm, WorkingTimeFormSet
from services.models import Service
from services.forms import ServiceForm


class WorkingTimeInline(admin.StackedInline):
    model = WorkingTime
    extra = 7
    max_num = 7
    form = WorkingTimeForm
    formset = WorkingTimeFormSet


class ServicesInline(admin.StackedInline):
    model = Service
    extra = 1
    form = ServiceForm


class ShopAdmin(admin.ModelAdmin):
    inlines = [ServicesInline, WorkingTimeInline]

    list_display = ('name', 'description', 'location', 'owner')
    readonly_fields = ('owner', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change or not obj.owner:
            try:
                obj.owner = request.user.get_account()
            except Exception as e:
                print(f"Error assigning owner: {e}")

        super().save_model(request, obj, form, change)


admin.site.register(Shop, ShopAdmin)
