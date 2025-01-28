from django.db import models
from .validators.telephone import validate_phone_number

class University(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="Universitet nomi"
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    class DegreeVariations(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER = 'master', 'Magistr'
        PHD = 'phd', 'Doktorantura'

    fullname = models.CharField(
        max_length=120,
        verbose_name="F.I.Sh"
    )
    degree = models.CharField(
        max_length=120,
        verbose_name="Talim turi",
        choices=DegreeVariations.choices,
        default=DegreeVariations.BACHELOR
    )
    university = models.ForeignKey(
        to='University',
        related_name='Universitet',
        on_delete=models.PROTECT
    )
    phone = models.CharField(
        max_length=25,
        validators=[validate_phone_number]
    )
    contract_amount = models.IntegerField(
        verbose_name="Kontrakt summasi"
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Sana"

    )

    def __str__(self):
        return self.fullname



class Sponsor(models.Model):
    class SponsorStatus(models.TextChoices):
        MODERATION = 'moderation', 'Moderatsiy'
        NEW = 'new', 'Yangi'
        APPROVED = 'approved', 'Tasdiqlangan'
        CANCELLED = 'cancelled', 'Bekor qilingan'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Naqd pul'
        CARD = 'card', 'Karta orqali'
        BANK_TRANSFER = 'bank_transfer', 'Bank oʻtkazmasi'
        OTHER = 'other', 'Boshqa'

    class SponsorType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Jismoniy shaxs'
        LEGAL_ENTITY = 'legal_entity', 'Yuridik shaxs'

    # class CollectedAmount(models.IntegerChoices):
    #     _1000000 = 1000000, '1 000 000'
    #     _5000000 = 5000000, '5 000 000'
    #     _7000000 = 7000000, '7 000 000'
    #     _10000000 = 10000000, '10 000 000'
    #     _30000000 = 30000000, '30 000 000'
    #     _50000000 = 50000000, '50 000 000'

    full_name = models.CharField(
        max_length=120,
        verbose_name="F.I.Sh"
    )
    phone = models.CharField(
        max_length=25,
        validators=[validate_phone_number],
        verbose_name="Telefon raqam"
    )
    collected_amount = models.IntegerField(
        # choices=CollectedAmount.choices,
        verbose_name="Homiylik summasi"
    )
    org_name = models.CharField(
        max_length=120,
        verbose_name="Tashkilot nomi",
        blank=True,
        null=True
    )
    sponsor_type = models.CharField(
        max_length=120,
        choices=SponsorType.choices,
        verbose_name="Homiy turi",

    )
    status = models.CharField(
        max_length=120,
        choices=SponsorStatus.choices,
        default=SponsorStatus.NEW,
        verbose_name="Holat"
    )
    payment_method = models.CharField(
        max_length=120,
        choices=PaymentMethod.choices,
        verbose_name="To‘lov turi",
        null=True
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Sana"
    )

    def __str__(self):
        return self.full_name



class SponsorStudent(models.Model):
    student = models.ForeignKey(
        to='Student',
        related_name='sponsored_students',
        on_delete=models.DO_NOTHING,
        verbose_name="Talaba"
    )
    sponsor = models.ForeignKey(
        to='Sponsor',
        related_name='sponsored_students',
        on_delete=models.DO_NOTHING,
        verbose_name="Homiy"
    )
    amount = models.IntegerField(
        default=0
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Sana"
    )

    def __str__(self):
        return f"{self.sponsor} → {self.student} ({self.amount})"


