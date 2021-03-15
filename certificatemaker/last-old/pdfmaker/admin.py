from django.contrib import admin

# Register your models here.


from .models import Document, HTMLTemplate

class DocumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Document, DocumentAdmin)



class HTMLTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(HTMLTemplate, HTMLTemplateAdmin)







