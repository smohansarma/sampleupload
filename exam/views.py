from django.shortcuts import render,redirect, get_object_or_404
import random
from django.contrib import messages
from .models import *
import streamlit as st
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .utils import render_to_pdf
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error generating PDF", status=400)

def download_candidates_pdf(request, candidate_id, date, test_type):
    # Fetch your dynamic data here
    results=Result.objects.filter(cid=candidate_id,created_at=date,test_name=test_type)
    data=Emp.objects.get(id=candidate_id)
    

    context = {
       
        'name': data.name,
        'datas': results,
        'candidate_id': candidate_id,
        'date': date,
        'test_type': test_type,  # Capitalize the test type for better presentation
    }

    pdf = render_to_pdf('pdf_result.html', context)  # Match the template name
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result.pdf"'
        return response
    return HttpResponse("PDF generation failed", status=500)


cn=0
aptitude=True
def home(request):
    return render(request,'index.html')

@csrf_exempt # !!! IMPORTANT: Only for testing. Remove in production and use @require_POST or CsrfViewMiddleware
def login(request):
    if request.method == 'POST':
        # Process form submission
        print("Received POST request!")

        form_data = {}
        errors = {}

        # --- Section 1: Personal Information ---
        form_data['name'] = request.POST.get('name')
        if not form_data['name']:
            errors['name'] = "Full Name is required."

        # Number validation: Must be an integer and exactly 10 digits
        number_str = request.POST.get('number')
        if not number_str:
            errors['number'] = "Number is required."
        elif not number_str.isdigit():
            errors['number'] = "Number must contain only digits."
        elif len(number_str) != 10:
            errors['number'] = "Please enter a 10-digit number."
        else:
            form_data['number'] = int(number_str)

        # Date of Birth validation
        form_data['dob'] = request.POST.get('dob')
        if not form_data['dob']:
            errors['dob'] = "Date of Birth is required."

        # Gender validation
        form_data['gender'] = request.POST.get('gender')
        if form_data['gender'] not in [choice[0] for choice in Emp.GENDER_CHOICES]:
            errors['gender'] = "Invalid Gender selection."

        # Marital Status validation
        form_data['marital_status'] = request.POST.get('maritalStatus')
        if form_data['marital_status'] not in [choice[0] for choice in Emp.MARITAL_STATUS_CHOICES]:
            errors['marital_status'] = "Invalid Marital Status selection."

        # Nationality validation
        form_data['nationality'] = request.POST.get('nationality')
        if not form_data['nationality']:
            errors['nationality'] = "Nationality is required."

        # Blood Group validation
        form_data['blood_group'] = request.POST.get('bloodGroup')
        if form_data['blood_group'] not in [choice[0] for choice in Emp.BLOOD_GROUP_CHOICES]:
            errors['blood_group'] = "Invalid Blood Group selection."

        # --- Section 2: Application Details ---
        form_data['position_applied'] = request.POST.get('positionApplied')
        if not form_data['position_applied']:
            errors['position_applied'] = "Position Applied For is required."

        form_data['department'] = request.POST.get('department')
        if form_data['department'] not in [choice[0] for choice in Emp.DEPARTMENT_CHOICES]:
            errors['department'] = "Invalid Department selection."

        # --- Section 3: Professional Details ---
        # Setting default value of None (null) if not provided
        form_data['basic_qualification'] = request.POST.get('basicQualification') or None
        form_data['pg_degree_name'] = request.POST.get('pgDegreeName') or None
        form_data['pg_category'] = request.POST.get('pgCategory') or None
        form_data['pg_passed_out'] = request.POST.get('pgPassedOut') or None


        # Year of graduation validation: Optional field with default null value
        form_data['year_of_graduation'] = request.POST.get('yearOfGraduation') or None
        if form_data['year_of_graduation'] and (not form_data['year_of_graduation'].isdigit() or len(form_data['year_of_graduation']) != 4):
            errors['year_of_graduation'] = "Year of Graduation must be a 4-digit number."

        # Total experience validation: Optional field with default null value
        form_data['total_experience'] = request.POST.get('totalExperience') or None

        # Optional fields for experience and skills
        form_data['relevant_experience'] = request.POST.get('relevantExperience') or None
        form_data['skills_certifications'] = request.POST.get('skillsCertifications') or None

        # --- Section 4: Document Submission ---
        form_data['resume_upload'] = request.FILES.get('resumeUpload')
        if not form_data['resume_upload']:
            errors['resume_upload'] = "Resume upload is required."

        form_data['photo_upload'] = request.FILES.get('photoUpload')
        if not form_data['photo_upload']:
            errors['photo_upload'] = "Passport Size Photo upload is required."

        form_data['highest_degree_type'] = request.POST.get('highestDegreeType')
        if form_data['highest_degree_type'] not in [choice[0] for choice in Emp.DEGREE_TYPE_CHOICES]:
            errors['highest_degree_type'] = "Invalid Highest Degree Type selection."

        form_data['degree_certificate_upload'] = request.FILES.get('degreeCertificateUpload')
        if not form_data['degree_certificate_upload']:
            errors['degree_certificate_upload'] = "Degree Certificate upload is required."

        # Payslip upload (optional)
        form_data['payslip_upload'] = request.FILES.get('payslipUpload')  # Optional field

        # Check for errors
        if errors:
            print("Form errors:", errors)
            return JsonResponse({'status': 'error', 'message': 'Validation failed', 'errors': errors}, status=400)

        # If validation passes, create and save the Emp instance
        try:
            # Check if a record already exists with the same name and number
            existing_client = Emp.objects.filter(name=form_data['name'], number=form_data['number']).first()
            if existing_client:
                # If found, update the count and return response
                existing_client.count += 1
                existing_client.save()
                request.session['customer_num'] = existing_client.id
                return render(request, 'technical.html')

            # Otherwise, create a new Emp instance with null values where applicable
            new_client = Emp(
                name=form_data['name'],
                number=form_data['number'],
                dob=form_data['dob'],
                gender=form_data['gender'],
                marital_status=form_data['marital_status'],
                nationality=form_data['nationality'],
                blood_group=form_data['blood_group'],
                position_applied=form_data['position_applied'],
                department=form_data['department'],
                basic_qualification=form_data['basic_qualification'],
                year_of_graduation=form_data['year_of_graduation'],
                current_employer=form_data.get('current_employer', None),  # Optional
                total_experience=form_data['total_experience'],
                relevant_experience=form_data['relevant_experience'],
                skills_certifications=form_data['skills_certifications'],
                resume_upload=form_data['resume_upload'],
                photo_upload=form_data['photo_upload'],
                highest_degree_type=form_data['highest_degree_type'],
                pg_degree_name=form_data['pg_degree_name'],
                pg_category=form_data['pg_category'],
                pg_passed_out=form_data['pg_passed_out'],
                degree_certificate_upload=form_data['degree_certificate_upload'],
                payslip_upload=form_data['payslip_upload'],  # Optional
            )
            new_client.save()
            request.session['customer_num'] = new_client.id
            return render(request, 'index.html')

        except Exception as e:
            print(f"Error saving client: {e}")
            return JsonResponse({'status': 'error', 'message': f'Server error: {e}'}, status=500)

    else:
        # Render the form for GET requests
        return render(request, 'gform.html')

# def login(request):
    global cn
    if request.method=='POST':
        name=request.POST.get('name')
        number=request.POST.get('number')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        marital_status=request.POST.get('maritalStatus')
        nationality=request.POST.get('nationality')
        position_applied=request.POST.get('positionApplied')
        department=request.POST.get('department')
        highest_qualification=request.POST.get('highestQualification')
        year_of_graduation=request.POST.get('yearOfGraduation')
        current_employer=request.POST.get('currentEmployer')
        total_experience=request.POST.get('totalExperience')
        relevent_experience=request.POST.get('releventExperience')
        skills_certification=request.POST.get("skillsCertification")
        resume_upload=request.POST.get('resumeUpload')
        photo_upload=request.POST.get("photoUpload")
        highest_degree_type=request.POST.get('highestDegreeType')
        degree_certificate_upload=request.POST.get('degreeCertificateUpload')
        is_experience=request.POST.get('isExperience')
        payslip_upload=request.POST.get('payslipUpload')
        

        if len(number)!=10:
            messages.warning(request,"Number Should be in 10 Digit")
            return render(request,'form.html')
            
        try:
            re=Emp.objects.get(name=name,number=number,dob=dob,gender=gender,
            marital_status=marital_status,
            nationality=nationality,
            position_applied=position_applied,
            department=department,
            highest_qualification=highest_qualification,
            year_of_graduation=year_of_graduation,
            current_employer=current_employer,
            total_experience=total_experience,
            relevent_experience=relevent_experience,
            skills_certification=skills_certification,
            resume_upload=resume_upload,
            photo_upload=photo_upload,
            highest_degree_type=highest_degree_type,
            degree_certificate_upload=degree_certificate_upload,
            is_experience=is_experience,
            payslip_upload=payslip_upload)
            re.count+=1
            re.save()
            #messages.warning(request,"Already Register")
            request.session['customer_num']=re.id
            return render(request,'technical.html')
        except:
            new_client=Emp(name=name,number=number)
            new_client.count+=1
            new_client.save()
            cn=number
            request.session['customer_num']=new_client.id
            return render(request,"index.html")
            
    return render(request,'form.html')

correct=[]
mark=0
ques=[]
o1=[]
o2=[]
o3=[]
o4=[]
def q1(request):
    print(request.session.get('customer_num'))
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if aptitude:
        if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='aptitude')
                ques.save()

            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.score=mark
                dd.save()
                print("mark",mark)
                mark=0
                aptitude=False
                #correct.clear()
                return redirect('/home')
            except:
                print('error')
                return redirect('/home')
    else:
        messages.warning(request,"Already done your Aptitude exam")
        return render(request,'index.html')    


    unique_number=random.sample(range(1,18),10)
    data=QA.objects.filter(id__in=unique_number)
    correct = QA.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=QA.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=QA.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=QA.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=QA.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=QA.objects.filter(id__in=unique_number).values_list('o4',flat=True)
    
    

    return render(request,'ques.html',{'values':data,'name':'Aptitude'})
    
    

def technical(request):
    global aptitude
    if aptitude==False:
        return render(request,'technical.html')
    else:
        messages.warning(request,"Please finish Aptitude exam First")
        return render(request,'index.html')   

def developer(request):
    return render(request,'developer.html')

#Python
def python(request):
    
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1
            
            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='python')
                ques.save()
                print(i,j,k)
            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='python'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                correct=[]
                ques=[]
                aptitude=True
                return render(request,'thankyou.html')
            except:
                 print('error')
                 return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=PM.objects.filter(id__in=unique_number)
    correct = PM.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=PM.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=PM.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=PM.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=PM.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=PM.objects.filter(id__in=unique_number).values_list('o4',flat=True)


    
    print(correct)
    
    

    return render(request,'ques.html',{'values':data,'name':'Python'})
    



def sql(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Sql')
                ques.save()

            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='Sql'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                request.session.flush()
                #correct.clear()
                aptitude=True
                return render(request,'thankyou.html')
            except:
                print('error')
                return render(request,'login.html')    


    unique_number=random.sample(range(1,20),10)
    data=Sql.objects.filter(id__in=unique_number)
    correct = Sql.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Sql.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Sql.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Sql.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Sql.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Sql.objects.filter(id__in=unique_number).values_list('o4',flat=True)    
    

    return render(request,'ques.html',{'values':data,'name':'Sql'})

#Java
def java(request):
    
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Java')
                ques.save()

            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='Java'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                #correct.clear()
                aptitude=True
                return render(request,'thankyou.html')
            except:
                 print('error')
                 return render(request,'login.html')    


    unique_number=random.sample(range(1,25),10)
    data=JM.objects.filter(id__in=unique_number)
    correct = JM.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=JM.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=JM.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=JM.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=JM.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=JM.objects.filter(id__in=unique_number).values_list('o4',flat=True)
    
    

    return render(request,'ques.html',{'values':data,'name':'Java'})

def hardware(request):
    return render(request,'hardware.html')

#CCTV
def cctv(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='cctv')
                ques.save()

            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='cctv'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                #correct.clear()
                aptitude=True
                return  render(request,'thankyou.html')
            except:
                 print('error')
                 return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=Cctv.objects.filter(id__in=unique_number)
    correct = Cctv.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Cctv.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Cctv.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Cctv.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Cctv.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Cctv.objects.filter(id__in=unique_number).values_list('o4',flat=True)
    
    

    return render(request,'ques.html',{'values':data,'name':'CCTV'})

def networking(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Networking')
                ques.save()

            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='Networking'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                #correct.clear()
                aptitude=True
                return render(request,'thankyou.html')
            except:
                 print('error')
                 return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=Networking.objects.filter(id__in=unique_number)
    correct = Networking.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Networking.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Networking.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Networking.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Networking.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Networking.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'Networking'})

def router(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Router')
                ques.save()

            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='Router'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                aptitude=True
            #correct.clear()
                return render(request,'thankyou.html')
            except:
                print('error')
                return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=Router.objects.filter(id__in=unique_number)
    correct = Router.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Router.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Router.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Router.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Router.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Router.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'Router'})

def server(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1
            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Server')
                ques.save()

            # try:
            dd=Emp.objects.get(id=request.session.get('customer_num'))
            dd.topic='Server'
            dd.tech_score=mark
            dd.save()
            print("mark",mark)
            mark=0
            aptitude=True
            #correct.clear()
            return render(request,'thankyou.html')
            # except:
            #     print('error')
            #     return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=Server.objects.filter(id__in=unique_number)
    correct = Server.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Server.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Server.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Server.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Server.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Server.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'Server'})

def photoshop(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Photoshop')
                ques.save()

            # try:
            dd=Emp.objects.get(id=request.session.get('customer_num'))
            dd.topic='Photoshop'
            dd.tech_score=mark
            dd.save()
            print("mark",mark)
            mark=0
            #correct.clear()
            aptitude=True
            return render(request,'thankyou.html')
            # except:
            #     print('error')
            #     return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=Photoshop.objects.filter(id__in=unique_number)
    correct =Photoshop.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=PM.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Photoshop.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Photoshop.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Photoshop.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Photoshop.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'Photoshop'})

#FLASH
def flash(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Flash')
                ques.save()

            # try:
            dd=Emp.objects.get(id=request.session.get('customer_num'))
            dd.topic='Flash'
            dd.tech_score=mark
            dd.save()
            print("mark",mark)
            mark=0
            #correct.clear()
            aptitude=True
            return render(request,'thankyou.html')
            # except:
            #     print('error')
            #     return render(request,'login.html')    


    unique_number=random.sample(range(1,30),10)
    data=Flash.objects.filter(id__in=unique_number)
    correct = Flash.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Flash.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Flash.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Flash.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Flash.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Flash.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'Flash'})
     

#CANVA
def canva(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='Canva')
                ques.save()

            # try:
            dd=Emp.objects.get(id=request.session.get('customer_num'))
            dd.topic='Canva'
            dd.tech_score=mark
            dd.save()
            print("mark",mark)
            mark=0
            #correct.clear()
            aptitude=True
            return render(request,'thankyou.html')
            # except:
            #     print('error')
            #     return render(request,'login.html')    


    unique_number=random.sample(range(1,10),3)
    data=Canva.objects.filter(id__in=unique_number)
    correct = Canva.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Canva.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Canva.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Canva.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Canva.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Canva.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'Canva'})


def digital(request):
    return render(request,'digital.html')
    
def hr(request):
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1

            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='HR')
                ques.save()

            # try:
            dd=Emp.objects.get(id=request.session.get('customer_num'))
            dd.topic='HR'
            dd.tech_score=mark
            dd.save()
            print("mark",mark)
            mark=0
            #correct.clear()
            aptitude=True
            return render(request,'thankyou.html')
            # except:
            #     print('error')
            #     return render(request,'login.html')    


    unique_number=random.sample(range(1,12),10)
    data=HR.objects.filter(id__in=unique_number)
    correct = HR.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=HR.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=HR.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=HR.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=HR.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=HR.objects.filter(id__in=unique_number).values_list('o4',flat=True)

    return render(request,'ques.html',{'values':data,'name':'HR'})

def admin2(request):
     client=Emp.objects.all
     return render(request,'admin.html',{'datas':client})

def result(request, id, date, topic):
    datas = Result.objects.filter(cid=id, created_at=date, test_name=topic)
    emp= Emp.objects.get(id=id)
    return render(request, 'result.html', {
        'datas': datas,
        'name': topic,
        'candidate_id': id,
        'date': date,
        'emp_name': emp.name,
    })


def accounts(request):
    
    global correct,mark,aptitude,ques,o1,o2,o3,o4
    if request.method=='POST':
            answers = []

            # Count how many answers you expect (e.g., 10)
            total_questions = 10

            for i in range(1, total_questions + 1):
                answer = request.POST.get(f'answer_{i}')
                answers.append(answer)

            
            
            for i,j in zip(answers,correct):
                print(i,j)
                if i.lower()==j:
                    mark+=1
            
            for i,j,k,l,m,n,o in zip(ques,correct,answers,o1,o2,o3,o4):
                ques=Result(q1=i,a1=j,s1=k,o1=l,o2=m,o3=n,o4=o,cid=request.session.get('customer_num'),test_name='accounts')
                ques.save()
                print(i,j,k)
            try:
                dd=Emp.objects.get(id=request.session.get('customer_num'))
                dd.topic='accounts'
                dd.tech_score=mark
                dd.save()
                print("mark",mark)
                mark=0
                correct=[]
                ques=[]
                aptitude=True
                return render(request,'thankyou.html')
            except:
                 print('error')
                 return render(request,'login.html')    


    unique_number=random.sample(range(1,30),10)
    data=Accounts.objects.filter(id__in=unique_number)
    correct = Accounts.objects.filter(id__in=unique_number).values_list('ans', flat=True)
    ques=Accounts.objects.filter(id__in=unique_number).values_list('question',flat=True)
    o1=Accounts.objects.filter(id__in=unique_number).values_list('o1',flat=True)
    o2=Accounts.objects.filter(id__in=unique_number).values_list('o2',flat=True)
    o3=Accounts.objects.filter(id__in=unique_number).values_list('o3',flat=True)
    o4=Accounts.objects.filter(id__in=unique_number).values_list('o4',flat=True)


    
    print(correct)
    
    

    return render(request,'ques.html',{'values':data,'name':'Accounts'})
def form(request):
    return render(request,'form.html')

def emp_detail(request, emp_id):
    emp = get_object_or_404(Emp, id=emp_id)
    at = Result.objects.filter(cid=emp_id, test_name='aptitude')
    t=emp.topic.lower()
    tt= Result.objects.filter(cid=emp_id, test_name=t)
    return render(request, 'emp_detail.html', {'emp': emp, 'at': at, 'tt': tt  })

def download_emp_detail_pdf(request, emp_id):
    emp = get_object_or_404(Emp, id=emp_id)
    at = Result.objects.filter( cid=emp_id, test_name='aptitude')
    t=emp.topic.lower()
    tt= Result.objects.filter(cid=emp_id, test_name=t)

    # Load the template
    template = get_template('emp_detail.html')
    
    # Correctly wrap the context in a dictionary
    html = template.render({'emp': emp, 'at': at, 'tt': tt})

    # Create a response object with PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="emp_{emp.name}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Error handling
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def emp_detail_client(request, emp_id):
    emp = get_object_or_404(Emp, id=emp_id)
    at = Result.objects.filter( cid=emp_id, test_name='aptitude')
    t=emp.topic.lower()
    tt= Result.objects.filter(cid=emp_id, test_name=t)

    # Load the template
    template = get_template('emp_detail_client.html')
    
    # Correctly wrap the context in a dictionary
    html = template.render({'emp': emp, 'at': at, 'tt': tt})

    # Create a response object with PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="emp_{emp.name}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Error handling
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response