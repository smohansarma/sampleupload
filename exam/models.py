from django.db import models
from django.utils.text import slugify
from django.template.defaultfilters import slugify



class QA(models.Model):
    question=models.TextField()
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50)

class Emp(models.Model):
    name = models.CharField(max_length=255)
    number=models.BigIntegerField()
    created_at=models.DateField(auto_now_add=True)
    score=models.IntegerField(null=True)
    topic=models.CharField(max_length=20,null=True)
    tech_score=models.IntegerField(null=True)
    count=models.IntegerField(default=0)
    slug=models.SlugField(unique=True)
    # Section 1: Personal Information
    dob = models.CharField(max_length=255)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Other', 'Other'),
    ]
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=100)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)

    # Section 2: Application Details
    position_applied = models.CharField(max_length=255)
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'), ('HR', 'HR'), ('Networking', 'Networking'),
        ('Digital Marketing', 'Digital Marketing'), ('Operations', 'Operations'),
        ('Sales', 'Sales'), ('Other', 'Other'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)


    # Section 3: Professional Details
    basic_qualification = models.CharField(max_length=255,null=True,blank=True)
    year_of_graduation = models.CharField(max_length=4,null=True,blank=True) # Changed to CharField for flexibility, though IntegerField is also possible
    current_employer = models.CharField(max_length=255,null=True,blank=True)
    total_experience = models.CharField(max_length=100,null=True,blank=True)  # Changed to CharField for flexibility
    relevant_experience = models.CharField(max_length=255, blank=True, null=True)
    skills_certifications = models.TextField(blank=True, null=True)

    # Section 4: Document Submission
    resume_upload = models.FileField(upload_to="picture")
    photo_upload = models.ImageField(upload_to="picture")
    DEGREE_TYPE_CHOICES = [
        ('UG', 'Undergraduate (UG)'),
        ('PG', 'Postgraduate (PG)'),
        ('Diploma', 'Diploma'),
    ]
    highest_degree_type = models.CharField(max_length=20, choices=DEGREE_TYPE_CHOICES,null=True)
    pg_degree_name=models.CharField(max_length=20,null=True,blank=True)
    pg_category=models.CharField(max_length=20,null=True,blank=True)
    pg_passed_out=models.BigIntegerField(null=True,blank=True)
    relevant_experience=models.TextField(blank=True,null=True)
    skills_certifications=models.TextField(blank=True,null=True)
    degree_certificate_upload = models.FileField(upload_to="picture",blank=True)

   # is_experienced = models.BooleanField() # True for Yes, False for No

    # These fields are conditionally required based on is_experienced
    payslip_upload = models.FileField(upload_to="picture", blank=True)

    def __str__(self):
        return self.full_name


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name + "_" + str(self.created_at))
        return super().save(*args,**kwargs) 
    def __str__(self):
        return self.name
    
class PM(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class JM(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Sql(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Cctv(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Networking(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Router(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Server(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Photoshop(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Flash(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class Canva(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)

class HR(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)


class Accounts(models.Model):
    question=models.TextField(max_length=500)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    ans=models.CharField(max_length=50,null=True)


class Result(models.Model):
    q1=models.TextField()
    a1=models.CharField(max_length=100,null=True)
    s1=models.CharField(max_length=100,null=True)
    o1=models.CharField(max_length=50)
    o2=models.CharField(max_length=50)
    o3=models.CharField(max_length=50)
    o4=models.CharField(max_length=50)
    test_name=models.CharField(max_length=50,null=True)
    cid=models.IntegerField(null=False)
    created_at=models.DateField(auto_now_add=True)
