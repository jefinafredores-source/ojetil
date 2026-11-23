from django.db import models


class Event(models.Model):

    EVENT_TYPES = [
        ('Conference', 'Conference'),
        ('Workshop', 'Workshop'),
        ('Sports', 'Sports'),
        ('Training', 'Training'),
        ('Seminar', 'Seminar'),
        ('Campaign', 'Campaign'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    event_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField(blank=True, null=True)

    location = models.CharField(max_length=200)

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPES,
        default='Conference'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )

    max_participants = models.PositiveIntegerField(default=100)

    participants = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def participant_percentage(self):
        if self.max_participants == 0:
            return 0

        return int(
            (self.participants / self.max_participants) * 100
        )
    
 

class ActivityCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    color = models.CharField(
        max_length=7,
        default="#2563eb",
        verbose_name="Category Color"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Activity Category"
        verbose_name_plural = "Activity Categories"

    def __str__(self):
        return self.name



class Activity(models.Model):

    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    activity_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200
    )

    category = models.ForeignKey(
        ActivityCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities'
    )

    event = models.ForeignKey(
        'Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming'
    )

    max_participants = models.PositiveIntegerField(
        default=100
    )

    participants = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to='activities/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    @property
    def participant_percentage(self):

        if self.max_participants == 0:
            return 0

        percentage = (
            self.participants /
            self.max_participants
        ) * 100

        return min(int(percentage), 100)
    
class EventInvitation(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='invitations'
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='invitations'
    )

    recipient_name = models.CharField(
        max_length=150,
        blank=True
    )

    recipient_email = models.EmailField()

    recipient_organization = models.CharField(
        max_length=200,
        blank=True
    )

    subject = models.CharField(max_length=200)

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    error_message = models.TextField(blank=True)

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.recipient_email   


