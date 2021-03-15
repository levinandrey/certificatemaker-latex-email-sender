from django.contrib import admin

# Register your models here.
from .models import Message, MessageStatus

class MessageAdmin(admin.ModelAdmin):
    pass
    list_display = ('slug', 'subject', 'email_from', 'reply_to', 'bcc_email',)
admin.site.register(Message, MessageAdmin)



class MessageStatusAdmin(admin.ModelAdmin):
    pass
    list_display = ('id', 'email_to', 'result_id', 'result_status', 'certificate',)
    list_filter = ('email_to', 'result_status',)
    search_fields = ('email',)

admin.site.register(MessageStatus, MessageStatusAdmin)

