from django.db import models

class Incident(models.Model):

    #
    # Severity choices
    #
    SEV1 = 'S1'
    SEV2 = 'S2'
    SEV3 = 'S3'
    SEV4 = 'S4'
    SEVERITY_CHOICES = (
        (SEV1, 'Severity 1'),
        (SEV2, 'Severity 2'),
        (SEV3, 'Severity 3'),
        (SEV4, 'Maintenance'),
    )
    severity = models.CharField(max_length=2,
                                choices=SEVERITY_CHOICES,
                                default=SEV4
    )

    #
    # Status Choices
    #
    STAT1 = 'S1'
    STAT2 = 'S2'
    STAT3 = 'S3'
    STAT4 = 'S4'
    STATUS_CHOICES = (
        (STAT1, 'One-Time'),
        (STAT2, 'Initial'),
        (STAT3, 'Update'),
        (STAT4, 'Final'),
    )
    status = models.CharField(max_length=2,
                                choices=STATUS_CHOICES,
                                default=STAT3
    )

    ticket   = models.CharField(max_length=20, blank=False, null=False)
    subject  = models.CharField(max_length=20, blank=False, null=False)
    description = models.TextField(max_length=120)
    incident_start = models.DateTimeField(verbose_name='Incident Start', blank=False, null=False)
    incident_end = models.DateTimeField(verbose_name='Incident End', null=True)
    impact   = models.CharField(max_length=120)
    next_update = models.DateTimeField(verbose_name='Next Update Time')

    # timestamps
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

class Log(models.Model):
    incident = models.ForeignKey(Incident)
    change_text = models.TextField(max_length=120, default="Initial entry")

    # timestamps
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
