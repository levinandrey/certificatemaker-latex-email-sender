from django.contrib import admin

# Register your models here.
from .models import PrePrintRecord







def generate_pdf_document(modeladmin, request, queryset):

    from latexprocessor.views import get_pdfs

    get_pdfs(queryset)


generate_pdf_document.short_description = "Generate Pdf using latex process"



def disable_gen_field(modeladmin, request, queryset):
    queryset.update(gen_cert=False)

disable_gen_field.short_description = "disable_gen_field"




from certificatestore.models import Certificate

class CerificatesInline(admin.TabularInline):
    model = Certificate

class PrePrintRecordAdmin(admin.ModelAdmin):
    pass
    inlines = [
        CerificatesInline,
    ]
    list_filter = ('process','gen_cert',)
    list_display = ('id', 'last_name', 'first_name', 'second_name', 'gender', 'email', 'attrs', 'process', 'created', 'updated','gen_cert',)
    actions = [generate_pdf_document, disable_gen_field,]
    search_fields = ('last_name', 'first_name', 'second_name', 'email', 'attrs',)
admin.site.register(PrePrintRecord, PrePrintRecordAdmin)
