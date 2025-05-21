from celery import shared_task
from django.core.mail import EmailMessage
from .utils import generate_pdf  # adjust as needed

@shared_task
def send_cv_pdf_to_email(cv_id, email):
    from .models import CV
    cv = CV.objects.get(id=cv_id)
    pdf = generate_pdf(cv)
    email_message = EmailMessage(
        subject="Your CV",
        body="Here is your CV in PDF format.",
        to=[email],
    )
    email_message.attach(f"cv_{cv_id}.pdf", pdf, "application/pdf")
    email_message.send()
