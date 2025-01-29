from rest_framework.urls import path

from .views import StudentView, UniversityView, SponsorStudentView, SponsorView

from .views import StudentListCreateAPIView, UniversityListCreateAPIView, SponsorListCreateAPIView, SponsorStudentListCreateAPIView, GetMonthStatsView, GetAmountStatsView

urlpatterns = [
    path('students/', StudentListCreateAPIView.as_view(), name="students"),
    path('universities/', UniversityListCreateAPIView.as_view(), name="universities"),
    path('student_sponsor/', SponsorStudentListCreateAPIView.as_view(), name="student_sponsor"),
    path('sponsors/', SponsorListCreateAPIView.as_view(), name='sponsor'),
    path('get_register_student_month/', GetMonthStatsView.as_view(), name='get_register_student_month'),
    path('amount_stats/', GetAmountStatsView.as_view(), name='amount_stats'),

]
