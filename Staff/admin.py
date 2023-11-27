from django.contrib import admin

from Staff.models import Staff , StaffEvaluationResult , PeerEvaluationResult

# Register your models here.
admin.site.register(Staff)
admin.site.register(StaffEvaluationResult)
admin.site.register(PeerEvaluationResult)