from django.shortcuts import render
from .models import QcmResult, Sensibilisation
from django.contrib.auth.decorators import login_required
from PhishingShark.models import Employes, EmailTracking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
import os
from datetime import datetime

# qcm db file:
QCM_FILE = os.path.join(os.path.dirname(__file__), "Qcm_Database", "qcm.json")


# helper functions here:


def load_questions():
    with open(QCM_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("questions", [])


def get_random_questions(n=20):
    all_questions = load_questions()
    if len(all_questions) < n:
        return all_questions
    return random.sample(all_questions, n)


# main functions here:


def training_page(request):

    # Get tracking UUID from URL
    tracking_uuid = request.GET.get("rid", "")
    employee_name = None
    employee_email = None

    # Try to find employee by tracking UUID
    if tracking_uuid:
        try:
            email_tracking = EmailTracking.objects.get(uuid=tracking_uuid)
            employee = email_tracking.employe
            employee_name = f"{employee.first_name} {employee.last_name}"
            employee_email = employee.email
        except EmailTracking.DoesNotExist:
            pass

    context = {
        "tracking_uuid": tracking_uuid,
        "employee_name": employee_name,
        "employee_email": employee_email,
    }

    return render(request, "sensibilisation/sens.html", context)


def qcm_page(request):
    tracking_uuid = request.GET.get("rid", "")

    # Get employee info from tracking UUID
    employee_name = None
    employee_matricule = None

    if tracking_uuid:
        try:
            email_tracking = EmailTracking.objects.get(uuid=tracking_uuid)
            employee = email_tracking.employe
            employee_name = f"{employee.first_name} {employee.last_name}"
            employee_matricule = employee.matricule
        except EmailTracking.DoesNotExist:
            pass

    # Get 20 random questions
    questions = get_random_questions(20)

    # Store questions in session for scoring
    request.session["quiz_questions"] = questions
    request.session["employee_matricule"] = employee_matricule
    request.session["tracking_uuid"] = tracking_uuid

    context = {
        "questions": questions,
        "employee_name": employee_name,
        "tracking_uuid": tracking_uuid,
        "total_questions": len(questions),
    }

    return render(request, "qcm/evaluation_qcm.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def cal_qcm_result(request):
    try:
        data = json.loads(request.body)
        answers = data.get("answers", {})

        # Get questions from session
        questions = request.session.get("quiz_questions", [])
        employee_matricule = request.session.get("employee_matricule", "")
        tracking_uuid = request.session.get("tracking_uuid", "")

        if not questions:
            return JsonResponse({"error": "No questions found"}, status=400)

        # Calculate score
        score = 0
        total = len(questions)
        results = []

        for q in questions:
            q_id = str(q["id"])
            user_answer = int(answers.get(q_id, -1))
            correct_answer = q["reponse"]
            is_correct = user_answer == correct_answer

            if is_correct:
                score += q.get("points", 1)

            results.append(
                {
                    "id": q["id"],
                    "question": q["question"],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                    "options": q["options"],
                    "points": q.get("points", 1),
                }
            )

        # Calculate percentage
        max_score = sum(q.get("points", 1) for q in questions)
        percentage = round((score / max_score) * 100, 2) if max_score > 0 else 0

        # Save to database (QcmResult)
        if employee_matricule:
            # Check if employee already has a result
            existing_result = QcmResult.objects.filter(
                employee_matricule=employee_matricule
            ).first()

            if existing_result:
                # Update existing
                existing_result.score = percentage
                existing_result.totale_qcm_taken += 1
                existing_result.start_at = datetime.now().time()
                existing_result.finish_at = datetime.now().time()
                existing_result.save()
            else:
                # Create new
                QcmResult.objects.create(
                    employee_matricule=employee_matricule,
                    score=percentage,
                    start_at=datetime.now().time(),
                    finish_at=datetime.now().time(),
                    totale_qcm_taken=1,
                )

        # Update EmailTracking status
        if tracking_uuid:
            try:
                email_tracking = EmailTracking.objects.get(uuid=tracking_uuid)
                email_tracking.status = "TRAINING_COMPLETED"
                email_tracking.save()
            except EmailTracking.DoesNotExist:
                pass

        # Clear session
        request.session.pop("quiz_questions", None)
        request.session.pop("employee_matricule", None)

        return JsonResponse(
            {
                "score": score,
                "total": total,
                "percentage": percentage,
                "results": results,
                "passed": percentage >= 80,
                "message": "Quiz completed successfully!",
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def qcm_result(request):
    return render(request, "sensibilisation/qcm_result.html")
