from rest_framework.urls import path

from .views import StudentView, UniversityView, SponsorStudentView, SponsorView

from .views import StudentListCreateAPIView, UniversityListCreateAPIView, SponsorListCreateAPIView, SponsorStudentListCreateAPIView

urlpatterns = [
    path('students/', StudentListCreateAPIView.as_view(), name="students"),
    path('universities/', UniversityListCreateAPIView.as_view(), name="universities"),
    path('student_sponsor/', SponsorStudentListCreateAPIView.as_view(), name="student_sponsor"),
    path('sponsors/', SponsorListCreateAPIView.as_view(), name='sponsor')

]