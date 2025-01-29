from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.validators import ValidationError

from .models import Student, University, Sponsor, SponsorStudent
from .serializers import StudentSerializerPOST, StudentSerializerGET, UniversitySerializer, SponsorSerializerGET, SponsorSerializerPOST, StudentSponsorSerializerGET, StudentSponsorSerializerPOST
from rest_framework import  generics
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .service import get_students_registrate_month, get_sponsors_registrate_month,get_sponsors_collected_amount, get_students_contract_amount, get_remaining_contract_amount


from .service import MonthStatsService


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['fullname']
    filterset_fields = ['degree', 'university']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentSerializerGET
        return StudentSerializerPOST

    def get_queryset(self):
        query = super().get_queryset()
        date_from = self.request.query_params.get("date_from", None)
        date_to = self.request.query_params.get("date_to", None)

        obj = {}
        if date_from:
            try:
                obj['date__gte'] = datetime.strptime(date_from, '%Y-%m-%d').date()
            except:
                raise ValueError("Invalid format for 'date_from'. Expected format: YYYY-MM-DD.")

        if date_to:
            try:
                obj['date__lte'] = datetime.strptime(date_to, '%Y-%m-%d').date()
            except:
                raise ValueError("Invalid format for 'date_to'. Expected format: YYYY-MM-DD.")
        return query.filter(**obj)


class StudentView(APIView):
    def get(self, request, *args, **kwargs):
        filters = {}
        json_filter = {
            "filter": [
                ("degree", "all"),
                ("university", "all"),
            ]
        }
        get_type = request.GET.get('type')
        if get_type and get_type in json_filter:
            for json_param in json_filter[get_type]:
                param = request.GET.get(json_param[0], json_param[1])
                if not param == 'all' and not None:
                    filters[json_param[0]] = param

        students = Student.objects.filter(**filters) if filters else Student.objects.all()
        serializer = StudentSerializerGET(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializerPOST(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)


###########################################################################
#######             |               ||                          ############
######              |===============||                           ###########
#####               | /            \ |                            ##########
######              ||              ||                           ###########
#######             ||              ||                          ############
############################################################################
class UniversityListCreateAPIView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UniversitySerializer
        return UniversitySerializer


class UniversityView(APIView):
    def get(self, request):
        university = University.objects.all()
        serializer = UniversitySerializer(university, many=True)
        return Response(
                serializer.data,
                status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UniversitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )




###########################################################################
#######             |               ||                          ############
######              |===============||                           ###########
#####               | /            \ |                            ##########
######              ||              ||                           ###########
#######             ||              ||                          ############
############################################################################
class SponsorView(APIView):
    def get(self, request):
        json_types = {
            'filter': [
                ('status', 'all'),
                ('collected_amount', 'all'),
            ],
        }

        get_type = request.GET.get('type')

        filters = {}
        if get_type and get_type in json_types:
            for json_param in json_types[get_type]:
                param = request.GET.get(json_param[0], json_param[1])
                if not param == "all" and not None:
                    filters[json_param[0]] = param

        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from:
            try:
                filters['date__gte'] = datetime.strptime(date_from, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError({"error": "Invalid date_from format. Use YYYY-MM-DD."})

        if date_to:
            try:
                filters['date__lte'] = datetime.strptime(date_to, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError({"error": "Invalid date_to format. Use YYYY-MM-DD."})

        sponsor = Sponsor.objects.filter(**filters) if filters else Sponsor.objects.all()

        serializer = SponsorSerializerGET(sponsor, many=True)
        print(filters)
        return Response(
                serializer.data,
                status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = SponsorSerializerPOST(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class SponsorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_field = ['fullname', 'phone', 'org_name', '']
    filterset_field = ['sponsor_type', 'status', 'payment_method', 'collected_amount']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SponsorSerializerGET
        return SponsorSerializerPOST

    def get_queryset(self):
        query = super().get_queryset()
        date_from = self.request.query_params.get("date_from", None)
        date_to = self.request.query_params.get("date_to", None)

        obj = {}
        if date_from:
            try:
                obj['date__gte'] = datetime.strptime(date_from, '%Y-%m-%d').date()
            except:
                raise ValueError("Invalid format for 'date_from'. Expected format: YYYY-MM-DD.")

        if date_to:
            try:
                obj['date__lte'] = datetime.strptime(date_to, '%Y-%m-%d').date()
            except:
                raise ValueError("Invalid format for 'date_to'. Expected format: YYYY-MM-DD.")
        return query.filter(**obj)



###########################################################################
#######             |               ||                          ############
######              |===============||                           ###########
#####               | /            \ |                            ##########
######              ||              ||                           ###########
#######             ||              ||                          ############
############################################################################
class SponsorStudentView(APIView):
    def get(self, request):
        sponsors = StudentSponsorSerializerGET.objects.all()
        serializer = sponsors(sponsors, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSponsorSerializerPOST(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

class SponsorStudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = SponsorStudent.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['sponsor__full_name', 'student__fullname']
    filterset_fields = ['sponsor', 'student']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentSponsorSerializerGET
        return StudentSponsorSerializerPOST



    def get_queryset(self):
        query = super().get_queryset()
        date_from = self.request.query_params.get("date_from", None)
        date_to = self.request.query_params.get("date_to", None)

        obj = {}
        if date_from:
            try:
                obj['date__gte'] = datetime.strptime(date_from, '%Y-%m-%d').date()
            except:
                raise ValueError("Invalid format for 'date_from'. Expected format: YYYY-MM-DD.")

        if date_to:
            try:
                obj['date__lte'] = datetime.strptime(date_to, '%Y-%m-%d').date()
            except:
                raise ValueError("Invalid format for 'date_to'. Expected format: YYYY-MM-DD.")
        return query.filter(**obj)





###########################################################################
#######             |               ||                          ############
######              |===============||                           ###########
#####               | /            \ |                            ##########
######              ||              ||                           ###########
#######             ||              ||                          ############
############################################################################


"""
class GetMonthStatsView(APIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        data_student = get_students_registrate_month()
        data_sponsor = get_sponsors_registrate_month()
        get_sponsors_collected_amount()

        response_data = {
            "students": [{
                "month": student.get("month"),
                "total": student.get("total"),
            } for student in data_student],

            "sponsors": [{
                "month": sponsor.get("month"),
                "total": sponsor.get("total")
            } for sponsor in data_sponsor]
        }
        return Response(response_data)
"""


class GetAmountStatsView(APIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        sponsors_collected_amount = get_sponsors_collected_amount()
        students_contract_amount = get_students_contract_amount()
        remaining_contract_amount = get_remaining_contract_amount()

        response_data = {
            "sponsors_collected_amount": sponsors_collected_amount,
            "students_contract_amount": students_contract_amount,
            "remaining_contract_amount": remaining_contract_amount
        }

        return Response(response_data)

class GetMonthStatsView(APIView):
    serializer_class = None

    def get(self, request):
        return Response(
            MonthStatsService().get_sponsor_student_stats()
        )
