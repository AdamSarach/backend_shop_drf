from django.db import models


class Supplier(models.Model):
    """Keep suppliers' personal data."""
    sup_id = models.PositiveIntegerField(primary_key=True)
    sup_name = models.CharField(max_length=50, unique=True)
    sup_status = models.CharField(max_length=30, blank=True)
    sup_email = models.EmailField()
    sup_phone_number = models.IntegerField()
    sup_postal_code = models.CharField(max_length=10)
    sup_city = models.CharField(max_length=50)
    sup_address = models.CharField(max_length=70)

    def __str__(self):
        return self.sup_name

    @property
    def full_address(self):
        """The full way of addressing a supplier"""
        return '{}, {}, {} {}'.format(self.sup_name, self.sup_address, self.sup_postal_code, self.sup_city)
