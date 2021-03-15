from django.contrib import admin

# Register your models here.


from .models import Certificate, CertificateOrgy


from django.urls import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape

from django.utils.html import format_html

class CertificateAdmin(admin.ModelAdmin):
    pass


    list_display = ('id', 'url_certificate', 'parent_record', 'latex_process', 'created',  'orgy', 'filename', 'get_email', 'get_attrs',)


    search_fields = ('parent_record__last_name', 'parent_record__first_name', 'parent_record__second_name',)
    list_filter = ('latex_process', 'orgy',)

    def url_certificate(self, obj):
        return format_html('<a href="%s%s">%s</a>' % ('/media/certificates/', obj.filename, obj.filename))

    url_certificate.allow_tags = True
    url_certificate.short_description = 'url_certificate'


    def get_email(self, obj):
        if obj is None:
            return ''

        if obj.parent_record is None:
            return ''

        return obj.parent_record.email

    get_email.admin_order_field = 'email'
    get_email.short_description = 'Email'


    def get_attrs(self, obj):
        if obj is None:
            return ''

        if obj.parent_record is None:
            return ''

        return obj.parent_record.attrs

    get_attrs.admin_order_field = 'attrs'
    get_attrs.short_description = 'Attrs'
admin.site.register(Certificate, CertificateAdmin)





class CertificateOrgyAdmin(admin.ModelAdmin):
    pass

    list_display = ('id', 'created', )

admin.site.register(CertificateOrgy, CertificateOrgyAdmin)
