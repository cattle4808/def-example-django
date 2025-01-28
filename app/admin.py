from django.contrib import admin

from .models import Student, University, Sponsor, SponsorStudent

admin.site.register(Student)
admin.site.register(University)
admin.site.register(Sponsor)
admin.site.register(SponsorStudent)

