from django.contrib import admin

# Register your models here.


from .models import Template, Attachment, LatexProcess

class AttachmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attachment, AttachmentAdmin)




class TemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Template, TemplateAdmin)



class LatexProcessAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'template', 'attrs_names', 'created', 'updated','slug',)
admin.site.register(LatexProcess, LatexProcessAdmin)


