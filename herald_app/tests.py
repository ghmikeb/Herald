from django.test import TestCase

from django.db import IntegrityError
import datetime

from herald_app.models import Incident, Log

class HeraldAppModelTests(TestCase):

    #
    # Incident Test
    #
    def test_can_create_incident_and_retrieve_it(self):
        new_incident = Incident.objects.create(
            severity = 'S1',
            status   = 'S1',
            ticket   = 'GO-1234',
            subject  = 'Porkchop sammitches',
            description = 'My hair is on fire',
            incident_start    = datetime.datetime(2013, 11, 01, 22, 00, 00),
            impact   = 'All the things are down',
            next_update =  datetime.datetime(2013, 11, 01, 22, 15, 00)
        )

        incident = Incident.objects.all()[0]

        self.assertEqual(new_incident, incident)

    def test_create_log_entry_when_new_incident_is_created(self):
        new_incident = Incident.objects.create(
            severity = 'S1',
            status   = 'S1',
            ticket   = 'GO-1234',
            subject  = 'Porkchop sammitches',
            description = 'My hair is on fire',
            incident_start    = datetime.datetime(2013, 11, 01, 22, 00, 00),
            impact   = 'All the things are down',
            next_update =  datetime.datetime(2013, 11, 01, 22, 15, 00)
        )
        now = datetime.datetime.now()

        new_log = Log.objects.create(
            incident = new_incident
        )

        self.assertEqual(new_log.change_text, 'Initial entry')
        self.assertEqual(new_log.incident.ticket, 'GO-1234')

    def test_create_log_entry_will_create_a_created_at_timestamp(self):
        new_incident = Incident.objects.create(
            severity = 'S1',
            status   = 'S1',
            ticket   = 'GO-1234',
            subject  = 'Porkchop sammitches',
            description = 'My hair is on fire',
            incident_start    = datetime.datetime(2013, 11, 01, 22, 00, 00),
            impact   = 'All the things are down',
            next_update =  datetime.datetime(2013, 11, 01, 22, 15, 00)
        )
        now = datetime.datetime.now()

        new_log = Log.objects.create(
            incident = new_incident
        )

        self.assertEqual(new_log.change_text, 'Initial entry')
        self.assertEqual(new_log.incident.ticket, 'GO-1234')
        created_at = new_log.incident.created_at
        self.assertEqual(
            ( created_at.year, created_at.month, created_at.day,
              created_at.hour, created_at.minute ),
            ( now.year, now.month, now.day, now.hour, now.minute )
        )

    def test_modifying_log_entry_will_update_a_modified_at_timestamp(self):
        incident = Incident.objects.create(
            severity = 'S1',
            status   = 'S1',
            ticket   = 'GO-1234',
            subject  = 'Porkchop sammitches',
            description = 'My hair is on fire',
            incident_start    = datetime.datetime(2013, 11, 01, 22, 00, 00),
            impact   = 'All the things are down',
            next_update =  datetime.datetime(2013, 11, 01, 22, 15, 00)
        )

        new_log = Log.objects.create(
            incident = incident
        )

        self.assertEqual(new_log.change_text, 'Initial entry')
        self.assertEqual(new_log.incident.ticket, 'GO-1234')
        created_at = new_log.incident.created_at

        # wait a minute
        print "Waiting a minute"
        import time
        time.sleep(60)

        # Modify the incident
        incident.description = "It is less of an issue now"
        incident.severity = 'S2'
        incident.save()
        incident_update = incident.modified_at

        new_log = Log.objects.create(
            incident = incident,
            change_text = "Decreased severity"
        )

        self.assertEqual(new_log.incident.description, "It is less of an issue now")
        self.assertEqual(new_log.incident.severity, 'S2')
        self.assertNotEqual(
            (incident_update.year, incident_update.month, incident_update.day,
             incident_update.hour, incident_update.minute),
            ( created_at.year, created_at.month, created_at.day,
              created_at.hour, created_at.minute )
        )




