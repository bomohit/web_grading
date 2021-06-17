from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from django.contrib.auth.models import User, auth
from .models import Course, Class, Assignment, Student, Submission
import sys
from io import StringIO
import contextlib

# Create your views here.
# user = None
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print("{}{}".format(username, password))
        global user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print("user is not none")
            auth.login(request, user)
            print("user: {}".format(user.username))

            # TESTING CODE
            request.session['user_email'] = user.email
            request.session['user_is_staff'] = user.is_staff
            request.session['user_is_authenticated'] = user.is_authenticated

            return redirect("home")
            # return(home(request))
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def home(request):
    # cLass = Class.objects.all()
    course = Course.objects.all()
    # TESTING CODE
    try:
        User = request.session['user_is_authenticated']
        print("user log in")
    except:
        print("user not log in")
        return redirect("/")

    # Check if user currently log in or not
    if ongoing(request):
        return render(request, 'home.html', {'course': course})
    else:
        return render(request, 'index.html')

def selectionCourse(request):
    # code = request.POST['code']
    global code
    if request.method == "POST":
        code = request.POST['code']
        request.session['code'] = code
        print("post")
    else:
        code = request.session['code']

    # Check user is a staff or not
    if user.is_staff:
        cLass = Class.objects.all()
        print("code:{}".format(code))

        return render(request, 'home.html', {'class': cLass, 'code': code})

    else:
        studentEmail = user.email
        class_code = Student.objects.get(code=code, email=studentEmail).class_code
        assignment = Assignment.objects.filter(code=code, class_code=class_code)
        submitted = Submission.objects.filter(code=code, class_code=class_code, email=studentEmail)
        filterSubmitted = ""
        for Submitted in submitted:
            filterSubmitted += str(Submitted.assignment_id)
            filterSubmitted += ","
        print("class_code: {}".format(class_code))

        for reassign in assignment:
            try:
                reassign.grade = Submission.objects.get(assignment_id=reassign.id, code=code, class_code=class_code, email=studentEmail).grade
            except:
                pass

            reassign.id = "{},".format(reassign.id)
            print(reassign.id)

        global Code
        global Class_code
        Code = code
        Class_code = class_code

        for i in assignment:
            print(i.class_code)
        return render(request, 'home.html', {'assignment': assignment, 'code':code, 'class_code':class_code, 'submitted': filterSubmitted})

def selectionClass(request):
    assignment = Assignment.objects.all()
    # codeClass
    codeClass = (request.POST['codeClass']).split(",")
    code = codeClass[0]
    class_code = codeClass[1]
    assignment = Assignment.objects.filter(code=code, class_code=class_code)

    return render(request, 'home.html', {'assignment': assignment, 'code':code, 'class_code':class_code})

def uploadQuestion(request):
    assignment = Assignment.objects.all()
    code = request.POST['code']
    class_code = request.POST['class_code']
    title = request.POST['questionTitle']
    questionType = request.POST['typeOptions']
    today = date.today()
    myFile =request.FILES['myfile']
    myFile2 =request.FILES['myfile2']
    # handle_uploaded_file(myFile)

    print("{},{}".format(code,class_code))

    uploadQuestion = Assignment(code=code, class_code=class_code, title=title, date=today, location=myFile, type=questionType, location_sample=myFile2)
    uploadQuestion.save()

    return render(request, 'home.html', {'assignment': assignment, 'code':code, 'class_code':class_code})

def submitAssignment(request):
    assignment = Assignment.objects.all()
    assignment_id = request.POST['Assignment_id'].replace(',','')
    myFile = request.FILES['docfile']
    email = user.email
    print("submitAssignment:Success")
    grade = 0.0

    # Check assignment type
    assignment_type = Assignment.objects.get(id=assignment_id).type
    sample = Assignment.objects.get(id=assignment_id).location_sample
    if assignment_type == "if else":
        grade = gradeIf(myFile.read(), sample.read())
    elif assignment_type == "for loop":
        grade = gradeFor(myFile.read(), sample.read())
    elif assignment_type == "while loop":
        grade = gradeWhile(myFile.read(), sample.read())
    else:
        pass

    submission = Submission(assignment_id=assignment_id, code=Code, class_code=Class_code, email=email, location=myFile, grade=grade)
    submission.save()
    return render(request, 'home.html', {'assignment': assignment, 'code':Code, 'class_code':Class_code})
    return redirect("selectionCourse")

def gradeIf(file, sample):
    g = 0

    student_submission = getOutput(file)
    sample_answer = getOutput(sample)

    if "if" in str(file) and "else:" in str(file):
        g = 30
        if sample_answer in student_submission:
            g += 20
            try:
                exec(file)
                g += 50
            except:
                print("Error Happen")
    else:
        g = 0


    print("marks is: {}".format(g))
    return g

def gradeFor(file, sample):
    g = 0

    student_submission = getOutput(file)
    sample_answer = getOutput(sample)

    if "for" in str(file) and "in" in str(file):
        g = 30
        if sample_answer in student_submission:
            g += 20
            try:
                exec(file)
                g += 50
            except:
                print("Error Happen")
    else:
        g = 0


    print("marks is: {}".format(g))
    return g

def gradeWhile(file, sample):
    g = 0

    student_submission = getOutput(file)
    sample_answer = getOutput(sample)

    if "while" in str(file):
        g = 30
        if sample_answer in student_submission:
            g += 20
            try:
                exec(file)
                g += 50
            except:
                print("Error Happen")
    else:
        g = 0

    print("marks is: {}".format(g))
    return g

def getOutput(file):
    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    with stdoutIO() as s:
        exec(file)

    return s.getvalue()

def showlist(request):
    info = request.GET['asg'].split(",")
    submission = Submission.objects.filter(code=info[0], class_code=info[1], assignment_id=info[2])
    print("{},{},{}".format(info[0], info[1], info[2]))
    return render(request, 'list.html', {'submission': submission})

# Login Logic
def logout(request):
    auth.logout(request)
    try:
        global user
        del user
    except:
        pass

    return redirect("/")

def ongoing(request):
    is_exist = "user" in globals()
    valid = True
    if is_exist:
        if user.is_authenticated:
            print("userAuth:{}".format(user.is_staff))
            valid = True
        else:
            valid = False
    else:
        valid = False
    return valid
