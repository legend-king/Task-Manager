from django.contrib import admin
from .models import Task, TaskCategory, TaskMaterial
from django.db.models import Q

# Register your models here.
class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    autocomplete_fields = ['sub_task_of', 'category'
    ]

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'sub_tasks':
    #         kwargs['queryset'] = Task.objects.filter(category__user=request.user)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)
    
class TaskMaterialInline(admin.StackedInline):
    model = TaskMaterial
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed', 'created_at', 'updated_at')
    list_filter = ('category', 'completed')
    search_fields = ('title', 'description')
    autocomplete_fields = ('category', 'sub_task_of')
    inlines = [TaskInline,TaskMaterialInline]

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'sub_tasks':
    #         kwargs['queryset'] = Task.objects.filter(category__user=request.user)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(category__user=request.user)
        return qs


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title',)
    autocomplete_fields = ('user', 'sub_category_of')
    fields = ['title', 'sub_category_of',]
    inlines = [TaskInline]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('user','created_at', 'updated_at')
        return ['created_at', 'updated_at']

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'sub_categories':
    #         kwargs['queryset'] = TaskCategory.objects.filter(user=request.user)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs


@admin.register(TaskMaterial)
class TaskMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'reference_link','created_at', 'updated_at')
    list_filter = ('task',)
    search_fields = ('title', 'description')
    autocomplete_fields = ('task',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(task__category__user=request.user)
        return qs
