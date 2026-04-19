from django.db import models


# this is the quiz result class (the question are store in static json file: Qcm_Database/qcm.json)
class QcmResult(models.Model):
    employee_matricule = models.CharField(max_length=100, unique=True)

    # socre evaluate wiht (%), 20 question in totale
    score = models.PositiveIntegerField(default=0)

    # both in this format (hh:mm)
    # both can be use to calculate the totale time
    start_at = models.TimeField()
    finish_at = models.TimeField()

    # the amount of time the employees take the quiz
    totale_qcm_taken = models.IntegerField(default=0)

    def __str__(self):
        return self.score


class Sensibilisation(models.Model):
    employee_matricule = models.CharField(max_length=100)
    # totale time spen reading the Sensibilisation page (hh:mm)
    totale_time = models.TimeField()
