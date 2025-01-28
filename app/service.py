from django.db.models import Sum
from .models import Student, Sponsor, SponsorStudent

class StudentAggregator:
    def __init__(self, student_id):
        self.student_id = student_id

    def get_all_sponsors(self):
        return list(SponsorStudent.objects.filter(student=self.student_id).values('student', 'sponsor', 'amount').order_by('sponsor'))

    def allocated_amount(self) -> int:
        return SponsorStudent.objects.filter(student=self.student_id).aggregate(total=Sum('amount'))['total'] or 0

    def remainder_amount(self) -> int:
        try:
            contract_amount = Student.objects.filter(pk=self.student_id).values_list('contract_amount', flat=True).first()
            if contract_amount is None:
                raise ValueError("Contract amount not found for student.")

            allocated = self.allocated_amount()
            remainder = contract_amount - allocated

            return max(remainder, 0)
        except Exception as e:
            return 0


class SponsorAggregator:
    def __init__(self, sponsor_id):
        self.sponsor_id = sponsor_id

    def get_used_amount(self):
        return SponsorStudent.objects.filter(sponsor=self.sponsor_id).aggregate(used=Sum('amount'))['used'] or 0




class StudentSponsorAggregator:
    def __init__(self, sponsor_id):
        self.sponsor_id = sponsor_id

    # def check_amount(self):
    #     try:
    #         amount = Sponsor.objects.filter(pk=self.sponsor_id).values_list('collected_amount', flat=True).first()
    #         if amount is None:
    #             raise ValueError(f"Sponsor with ID {self.sponsor_id} not found.")
    #
    #         used_amount = SponsorStudent.objects.filter(sponsor=self.sponsor_id).aggregate(
    #             used=Sum('amount')
    #         )['used'] or 0
    #
    #         if used_amount > amount:
    #             raise ValueError(
    #                 f"Used amount ({used_amount}) exceeds collected amount ({amount}) for sponsor {self.sponsor_id}."
    #             )
    #
    #         return used_amount
    #     except Exception as e:
    #         print(f"Error in check_amount for sponsor {self.sponsor_id}: {e}")
    #         raise


    def check_used_amount(self, *args, **kwargs):
        sponsor = Sponsor.objects.filter(pk=self.sponsor_id).first()
        if not sponsor:
            raise ValueError(f"Sponsor with ID {self.sponsor_id} not found.")

        get_sponsor_used_amount = self.get_used_amount()
        get_collected_amount = sponsor.collected_amount
        get_amount = kwargs.get("amount", 0)


        if get_sponsor_used_amount + get_amount > get_collected_amount:
            raise ValueError(
                f"Insufficient funds. Sponsor has collected {get_collected_amount}, "
                f"already used {get_sponsor_used_amount}, and tried to allocate {get_amount}."
            )
        return True

    def get_used_amount(self):
        try:
            return SponsorStudent.objects.filter(sponsor=self.sponsor_id).aggregate(
                used=Sum('amount')
            )['used'] or 0
        except Exception as e:
            print(f"Error in get_used_amount for sponsor {self.sponsor_id}: {e}")
            return 0






# annotate, TruncMonth


