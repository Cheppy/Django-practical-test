from django.db import models

class CV(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.TextField(help_text="List your skills, separated by commas")
    projects = models.TextField(help_text="Describe your projects")
    contacts = models.TextField(help_text="Your contact information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
