from django.db import models
from django.utils import timezone




STATUS_CHOICES = ((1, "Active"), (0, "In-active"), (2, "Processing"),
                  (3, "Conflicted"), (4, "Error during processing"))
RENTAL_CHOICES = (
        (0, 'Non-negotiable'),
    )
    
FURNISHER_CHOICES = (
        (0, 'Unfurnished'),
        (1, 'Semi-furnished'),
        (2, 'Fully furnished'),
    )
    
APARTMENT_TYPE_CHOICES = (
        (0, 'Studio'),
        (1, '1 BHK'),
        (2, '2 BHK'),
        (3, '3 BHK'),
        (4, '4 BHK'),
    )
ROOM_TYPE_CHOICES = (
        (0, 'Single Room'),
        (1, 'Double Sharing'),
        (2, 'Triple Sharing'),
        (3, 'Dormitory'),
    )

FOOD_FACILITY_CHOICES = (
        (0, 'No'),
        (1, 'Yes'),
    )

# FURNISHING_CHOICES = (
#         (0, 'Unfurnished'),
#         (1, 'Semi-furnished'),
#         (2, 'Fully furnished'),
#     )
    
# APARTMENT_TYPE_CHOICES = (
#         (0, 'Studio'),
#         (1, '1 BHK'),
#         (2, '2 BHK'),
#         (3, '3 BHK'),
#         (4, '4 BHK'),
#     )

# Create your models here.
class SoftDeleteQuerySet(models.query.QuerySet):
    """
    QuerySet whose delete() does not delete items, but instead marks the
    rows as not active, by updating deleted_at field.
    """

    def delete(self):
        """
        Soft delete Method.
        """
        self.update(deleted_at=timezone.now())

    def hard_delete(self):
        """
        Permanent delete method.
        """
        return super(SoftDeleteQuerySet, self).delete()


class SoftDeleteManager(models.Manager):
    """
    Manager that returns a SoftDeleteQuerySet,
    to prevent object deletion.
    """

    def __init__(self, *args, **kwargs):
        self.active = kwargs.pop('active', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.active:
            return SoftDeleteQuerySet(self.model).filter(deleted_at=None)
        return SoftDeleteQuerySet(self.model)


class Abstract(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(active=False)

    # https://medium.com/@dineshs91/django-soft-delete-options-864082511918
    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class Countries(Abstract):

    name = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    version = models.IntegerField(default=0)
    added_by = models.IntegerField()
    updated_by = models.IntegerField()
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.name)


class States(Abstract):

    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Countries, related_name='country_id', null=True, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    version = models.IntegerField(default=0)
    added_by = models.IntegerField()
    updated_by = models.IntegerField()
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.name)
    

class Cities(Abstract):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(
        States, related_name='state_id', on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
   
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    version = models.IntegerField(default=0)
    added_by = models.IntegerField()
    updated_by = models.IntegerField()
    description = models.TextField(null=True)
    weightage = models.IntegerField(default=1)
    tags = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
    

class Areas(Abstract):

    name = models.CharField(max_length=1000)
    city = models.ForeignKey(
        Cities, on_delete=models.PROTECT, related_name='hops')
    area_name = models.TextField()
    version = models.IntegerField(default=0)
    area_name = models.TextField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    

    def __str__(self):
        return str(self.name)



class FullHouse(Abstract):
    
 
    name = models.CharField(max_length=255)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    buildup = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_tenants = models.CharField(max_length=255)
    furnisher = models.IntegerField(choices=FURNISHER_CHOICES)
    apartment_type = models.IntegerField(choices=APARTMENT_TYPE_CHOICES)
    ready_to_move = models.BooleanField(default=False)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    area = models.ForeignKey(Areas, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.name)
    

class PG(Abstract):
   

    name = models.CharField(max_length=255)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    room_type_available = models.IntegerField(choices=ROOM_TYPE_CHOICES)
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_tenants = models.CharField(max_length=255)
    posted_on = models.DateTimeField(auto_now_add=True)
    food_facility = models.IntegerField(choices=FOOD_FACILITY_CHOICES)
    gate_closing_time = models.TimeField()
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    area = models.ForeignKey(Areas, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.name)
    

class Flatmates(Abstract):
    
    name = models.CharField(max_length=255)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    buildup = models.DecimalField(max_digits=10, decimal_places=2)
    furnishing = models.IntegerField(choices=FURNISHER_CHOICES)
    apartment_type = models.IntegerField(choices=APARTMENT_TYPE_CHOICES)
    attached_bathroom = models.BooleanField(default=False)
    available_from = models.DateField()
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    area = models.ForeignKey(Areas, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.name)