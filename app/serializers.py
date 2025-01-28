from rest_framework import serializers
from .models import Student, Sponsor, University, SponsorStudent
from .service import StudentAggregator, SponsorAggregator, StudentSponsorAggregator


################################################################################################
################################################################################################
################################################################################################


class StudentSerializerPOST(serializers.ModelSerializer):
    # full_name = serializers.CharField(max_length=120)
    # degree = serializers.CharField(max_length=120)
    # university = serializers.IntegerField()
    # telephone = serializers.CharField(max_length=25)
    # contract_amount = serializers.IntegerField()

    class Meta:
        model = Student
        fields = '__all__'
        # fields = ('id', 'full_name', 'degree', 'university', 'telephone', 'contract_amount', 'date')
        extra_kwargs = {
            'date': {'read_only': True}
        }


class StudentSerializerGET(serializers.ModelSerializer):
    # sponsors = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'



    def to_representation(self, instance):
        representation = super().to_representation(instance)

        get_id_student = representation.get('id')
        obj = StudentAggregator(get_id_student).allocated_amount()
        representation['collected_amount'] = obj
        return representation


################################################################################################
################################################################################################
################################################################################################

class SponsorSerializerGET(serializers.ModelSerializer):
    # full_name = serializers.CharField(max_length=120)
    # telephone = serializers.CharField
    # collected_amount = serializers.IntegerField()
    # org_name = serializers.CharField(max_length=120)
    # sponsor_type = serializers.CharField(max_length=120)
    # status = serializers.CharField(max_length=120)
    # payment_method = serializers.CharField(max_length=120)

    class Meta:
        model = Sponsor
        exclude = ('payment_method', 'date')
        extra_kwargs = {
            'date': {'read_only': True},
            'status': {'read_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sponsor_id = representation.get('id')
        representation['used_amount'] = SponsorAggregator(sponsor_id=sponsor_id).get_used_amount()
        return representation







class SponsorSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        exclude = ('payment_method', 'date')
        extra_kwargs = {
            'date': {'read_only': True},
            'status': {'read_only': True}
        }

    def validate(self, attrs):
        sponsor_type = attrs.get("sponsor_type")
        org_name = attrs.get("org_name")


        if sponsor_type == "individual" and org_name:
            raise serializers.ValidationError({
                'org_name': "Organization name should not be provided for individuals."
            })

        if sponsor_type == "legal_entity" and not org_name:
            raise serializers.ValidationError({
                'org_name': "Organization name is required for legal entities."
            })

        return attrs




################################################################################################
################################################################################################
################################################################################################


class UniversitySerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=120)
    class Meta:
        model = University
        fields = '__all__'


################################################################################################
################################################################################################
################################################################################################


class StudentSponsorSerializerGET(serializers.ModelSerializer):
    # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    # sponsor = serializers.PrimaryKeyRelatedField(queryset=Sponsor.objects.all())
    # amount = serializers.IntegerField()
    class Meta:
        model = SponsorStudent
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sponsor_id = representation.get('sponsor')
        representation['used'] = StudentSponsorAggregator(sponsor_id).get_used_amount()
        return representation


class StudentSponsorSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = SponsorStudent
        fields = '__all__'

    def validate(self, attrs):
        sponsor = attrs.get('sponsor')
        if not sponsor:
            raise serializers.ValidationError({"sponsor": "Sponsor is required."})

        sponsor_id = sponsor.id
        amount = attrs.get('amount') or 0

        if int(amount) < 0:
            raise serializers.ValidationError({'amount': "Amount in not <0."})

        try:
            StudentSponsorAggregator(sponsor_id=sponsor_id).check_used_amount(amount=amount)
        except ValueError as e:
            raise serializers.ValidationError({"amount": str(e)})

        return attrs











