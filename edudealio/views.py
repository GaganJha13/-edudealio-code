from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import (
    generate_otp, send_otp_email,
    send_subscription_successful_email, send_signup_successful_email,
    send_message_successful_email, send_referee_successful_email,
    send_referrer_successful_email
)
from django.contrib.auth import authenticate, login, logout
from .models import (
    StandardizeTestModel, ActivityModel,
    ContactMessageModel, QuestionnaireModel,
    ClassModel, StudentDashboardDataModel, StudentPointsModel,
    OffersModel, StudentModel, SubscriptionModel, ReferralModel,
    UserProfileModel)
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
import os
import openai
from django.http import JsonResponse
import json
from django.utils.safestring import mark_safe
from django.forms import formset_factory

# check the user is admin or not


def is_admin(user):
    return user.is_authenticated and user.is_staff

# Create your views here.


class HomepageView(TemplateView):
    """Return homepage on API call"""
    template_name = "edudealio/homepage.html"


class loginView(View):
    """Return login page on API call"""

    def get(self, request):
        """Return login page on get request"""
        if request.user.is_authenticated:
            return redirect("homepage")
        else:
            return render(request, "edudealio/login.html")

    def post(self, request):
        """Return dashboard page on posting successful credentials"""
        username = request.POST["username"].lower()
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect("login")


def logoutpage(request):
    """Logging out the user"""
    logout(request)
    return redirect("login")


class RegisterView(View):
    """Return registration page on API call"""

    def get(self, request):
        """Return register page on get request"""
        if request.user.is_authenticated:
            return redirect("homepage")
        else:
            ref_code = request.GET.get('ref')
            request.session['ref_code'] = ref_code
            return render(request, "edudealio/register.html")

    def post(self, request):
        """return otp verification and Save data from register page on post request"""
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            username = request.POST.get("username").lower()
            email = request.POST.get("email").lower()
            request.session["username"] = username
            request.session["email"] = email
            request.session["password1"] = password1
            if User.objects.filter(email=email):
                messages.error(
                    request, "Sorry, but this email address is already registered. Try Sign in")
                return redirect("register")
            else:
                if User.objects.filter(username=username):
                    messages.error(
                        request, "Sorry, this username is already exists.")
                    return redirect("register")
                else:
                    otp = generate_otp()
                    request.session['otp'] = otp
                    send_otp_email(email, otp)
                    return redirect('verify')  
        else:
            messages.error(
                request, "Passwords do not match. Please try again.")
            return redirect("register")


class VerifyView(View):
    """Return the verification page"""

    def get(self, request):
        """Return verification page on get request"""
        email = request.session['email']
        context = {
            'email': email,
        }
        return render(request, "edudealio/verify.html", context)

    def post(self, request):
        """Return verification page on post request"""
        username = request.session['username']
        email = request.session['email']
        password1 = request.session['password1']
        otp = request.session['otp']
        user_otp = "".join([request.POST['value1'], request.POST['value2'], request.POST['value3'],
                           request.POST['value4'], request.POST['value5'], request.POST['value6']])
        if otp == user_otp:
            member = User.objects.create_user(
                username=username, email=email, password=password1)
            if request.session['ref_code']:
                try:
                    member.save()

                    # To add 5 points on referee and referrer's profile
                    current_user = User.objects.get(username=username)
                    referred_by = ReferralModel.objects.get(
                        referral_code=request.session['ref_code'])
                    refer_user = referred_by.user
                    user_profile_referral = UserProfileModel.objects.create(
                        user=current_user, referred_by=refer_user)
                    user_profile_referral.save()
                    points = 5
                    updatePoints(request, current_user, points)
                    updatePoints(request, refer_user, points)

                    # referee data for email
                    referee_name = current_user.username
                    referee_email = email

                    # referrer data for email
                    referrer_name = refer_user.username
                    referrer_email = refer_user.email

                    # after reference email
                    send_referee_successful_email(
                        referee_email, referee_name, referrer_name)
                    send_referrer_successful_email(
                        referrer_email, referee_name, referrer_name)
                except ReferralModel.DoesNotExist:
                    messages.error(request, "Incorrect referral code.")
            else:
                member.save()
            refer_code = ReferralModel.objects.create(user=member)
            refer_code.save()
            # check if the member's email is in subscription model or not.
            try:
                find_email = SubscriptionModel.objects.get(email=email)
            except SubscriptionModel.DoesNotExist:
                subscribe_member = SubscriptionModel.objects.create(
                    email=email)
                subscribe_member.save()
            send_signup_successful_email(email, username)
            messages.success(request, "Welcome "+username.title(
            )+"! Start exploring and enjoying all the great features our platform has to offer.")
            return redirect('login')
        else:
            messages.error(request, "Incorrect otp. Please try again.")


class SubscribeMemberView(View):
    """Subscribing user"""

    def post(self, request):
        email = request.POST['email']
        request.session['email'] = email
        try:
            find_email = SubscriptionModel.objects.get(email=email)
        except SubscriptionModel.DoesNotExist:
            subscribe_member = SubscriptionModel.objects.create(email=email)
            subscribe_member.save()
            send_subscription_successful_email(email)
            messages.success(
                request, "Welcome aboard! Your subscription is confirmed. Thank you for joining our community. You'll now receive our latest updates and news.")
        else:
            messages.error(request, "The email address you provided is already subscribed to our updates. If you have any questions or need assistance, please feel free to contact our support team.")
        return redirect("homepage")


@login_required(login_url='login')
def uploadmarksview(request):
    """Uploading the marks of students"""
    if request.method == "GET":
        student_form = StudentForm()
        custom_school_form = CustomSchoolForm()
        subject_percentage_formset = SubjectPercentageFormSet(
            prefix='subject_percentage')
        context = {
            'student_form': student_form,
            'subject_percentage_formset': subject_percentage_formset,
            'custom_school_form': custom_school_form,
        }
        return render(request, 'edudealio/upload_marks.html', context)
    elif request.method == "POST":
        student_form = StudentForm(request.POST, request.FILES)
        subject_percentage_formset = SubjectPercentageFormSet(
            request.POST, prefix='subject_percentage')
        print(subject_percentage_formset.total_form_count())
        if student_form.is_valid() and subject_percentage_formset.is_valid():
            student = student_form.save(commit=False)
            # Check if a custom school name is provided
            if student.school.name == 'other':
                custom_school_form = CustomSchoolForm(request.POST)
                if custom_school_form.is_valid():
                    custom_school_name = request.POST.get('custom_school_name')
                    if custom_school_name:
                        # Create a new school entry with the custom name
                        school, created = SchoolModel.objects.get_or_create(
                            name=custom_school_name)
                        student.school = school
            student.user = request.user
            student.save()
            student = StudentModel.objects.filter(user=request.user.id).last()
            is_formset_valid = subject_percentage_formset.is_valid()
            if is_formset_valid:
                for i, form in enumerate(subject_percentage_formset):
                    print(f"Cleaned data for form {i}: {form.cleaned_data}")
                    studentsubject = StudentSubjectModel.objects.create(
                        student=student,
                        subject=form.cleaned_data.get('subject'),
                        percentage=form.cleaned_data.get("percentage"),
                        student_class=student.student_class,
                        semester=student.semester
                    )
                    studentsubject.save()
            request_user = request.user
            updateUploadCount(request, request_user)
            points = 20
            updatePoints(request, request_user, points)
        else:
            print(student_form.errors)
        return redirect("dashboard")


@receiver(post_save, sender=User)
def create_user_points(sender, instance, created, **kwargs):
    if created:
        StudentDashboardDataModel.objects.create(
            user=instance, total_points=0, active_points=0, uploads=0, offers_avail=0)


@login_required(login_url='login')
def dashboardview(request):
    """Show the points earned in last week"""
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    date_joined = request.user.date_joined.date()

    # Retrieve points data for the last seven days
    points_data = StudentPointsModel.objects.filter(
        user=request.user,  # Adjust this to match your user retrieval logic
        date__range=[start_date, end_date]
    ).values('date', 'points')

    # Prepare data for the chart
    labels = []
    data = []

    for day in range(7):
        date_value = start_date + timedelta(days=day)
        date_label = (date_value).strftime("%Y-%m-%d")
        labels.append(date_label)
        points = points_data.filter(date=date_label).last()

        if points:
            previous_points = points['points']
            data.append(points['points'])
        else:
            if date_joined > date_value:
                points = 0
                previous_points = points
            elif day == 0:
                try:
                    from django.db.models import Max
                    points = StudentPointsModel.objects.filter(
                        user=request.user,
                        date__lt=start_date  # Retrieve points before this target_date
                    ).latest('date').points
                except StudentPointsModel.DoesNotExist:
                    points = StudentDashboardDataModel.objects.get(
                        user=request.user.id).active_points
                previous_points = points
            else:
                points = previous_points
            data.append(points)
    # offer model
    offers = OffersModel.objects.all()
    context = {
        'labels': labels,
        'data': data,
        'offers': offers,
    }
    return render(request, "edudealio/dashboard.html", context)


@login_required(login_url='login')
def questionnaireview(request):
    """Shows a page with questions to solve"""
    if request.method == "POST":
        questionnaire_form = QuestionnaireForm(request.POST)
        if questionnaire_form.is_valid():
            selected_topic = questionnaire_form.cleaned_data['topic'].name
            selected_class = questionnaire_form.cleaned_data['question_class'].name
            # collect the values of class and topic to add in data
            request.session['selected_topic'] = selected_topic
            request.session['selected_class'] = selected_class
        response_data = {"message": "Data received and processed successfully"}
        return JsonResponse(response_data)
    else:
        context = {
            "questionnaire_form": QuestionnaireForm,
        }
        return render(request, 'edudealio/questionnaire.html', context)

# To update upload count


def updateUploadCount(request, request_user):
    # update upload documents count on dashboard
    dashboard_data = StudentDashboardDataModel.objects.get(
        user=request_user.id)
    dashboard_data.uploads += 1
    dashboard_data.save()

# To update points in dashboard


def updatePoints(request, request_user, points):
    # update points on dashboard
    dashboard_points = StudentDashboardDataModel.objects.get(
        user=request_user.id)
    dashboard_points.active_points = int(
        dashboard_points.active_points) + int(points)
    request.session['active_points'] = dashboard_points.active_points
    dashboard_points.total_points = int(
        dashboard_points.total_points) + int(points)
    dashboard_points.save()

    # update points on graph
    try:
        student_graph_points = StudentPointsModel.objects.get(
            user=request.user, date=date.today())
        student_graph_points.points = request.session['active_points']
        student_graph_points.save()
    except StudentPointsModel.DoesNotExist:
        student_graph_points = StudentPointsModel.objects.create(
            user=request_user,
            points=request.session['active_points'])
        student_graph_points.save()


def mcqview(request):
    if request.method == "GET":
        # collect the value of class and topic
        selected_class = request.session['selected_class']
        selected_topic = request.session['selected_topic']

        # Load API key from an environment variable or secret management service
        openai.api_key = os.getenv("OPEN_API_SECRET_KEY")

        # prompt = f"Generate 5 multiple-choice questions with 4 choices with answers (using a,b,c,d for listing) on the topic of {selected_topic} for {selected_class} grade students  in a format like - '1. Which of the following is not a valid data type in Python?  a) String b) Integer c) Float d) Character  Answer: d) Character'."
        text_to_embed = f"Generate 5 multiple choice questions with four multiple choices (a,b,c,d) on {selected_topic} for {selected_class} grade students in format - '\n\n1) [Question statement]?\nExplanation: [Explanation text]. The correct answer is [Correct Option]) [Correct Answer].\na) [Option 1]\nb) [Option 2]\nc) [Option 3]\nd) [Option 4]'. Please explain each question by solving and confirm the correct answer for each question. Make sure the correct answer is to present in the options. Ensure the question is unique each time this prompt is called."
        
        # Define the prompt format for generating embeddings
        prompt = f"Embed: {text_to_embed}"
        
        print(prompt)
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Specify the GPT-3 engine
            prompt=prompt,
            max_tokens=600,  # Set the maximum number of tokens for the completion
            temperature=0.7  # Adjust the temperature parameter for diversity in output
        )
        print(completion)
        if completion.choices and completion.choices[0].text:
            uncleaned_mcq_questions_list = completion.choices[0].text.split(
            "\n\n")[1:]
            options_name = ['a)', 'b)', 'c)', 'd)']
            cleaned_mcqs_list = []
        else:
            print("Embeddings not found in the response.")
        if len(uncleaned_mcq_questions_list) == 5:
            for i, uncleaned_mcq_questions in enumerate(uncleaned_mcq_questions_list):
                uncleaned_mcq_question = uncleaned_mcq_questions.split("\n")
                mcq_question_dict = {'question': '',
                                     'options': [], 'correctAnswer': ''}
                for value in uncleaned_mcq_question:
                    if 'correct answer' in value and '?' not in value:
                        mcq_question_dict['correctAnswer'] = value.split(
                            "The correct answer is ")[1][:-1]
                    elif 'correct answer' not in value and 'Explanation' not in value and not any(option in value for option in options_name):
                        if '?' in value:
                            mcq_question_dict['question'] = value
                        else:
                            mcq_question_dict['question'] += "\n\n" + value
                    else:
                        for option in options_name:
                            if option in value:
                                mcq_question_dict['options'].append(value)
                cleaned_mcqs_list.append(mcq_question_dict)
            print(cleaned_mcqs_list)
        else:
            i = 0
            while i < len(uncleaned_mcq_questions_list):
                question = uncleaned_mcq_questions_list[i]
                uncleaned_options_list = uncleaned_mcq_questions_list[i + 1].split('\n')[
                    1:]
                options = [option for option in uncleaned_options_list if any(
                    option_name in option for option_name in options_name)]
                question += "\n\n" + "\n".join([option for option in uncleaned_options_list if not any(
                    option_name in option for option_name in options_name)])
                correct_answer = uncleaned_mcq_questions_list[i + 2]
                explanation = uncleaned_mcq_questions_list[i + 3]

                parsed_question = {
                    'question': question,
                    'options': options,
                    'correctAnswer': correct_answer,
                    # Extract explanation text
                    'explanation': explanation.split(': ', 1)[1]
                }

                cleaned_mcqs_list.append(parsed_question)
                i += 4
        mcq_data = mark_safe(json.dumps(cleaned_mcqs_list))
        context = {
            "mcq_data": mcq_data,
        }
        return render(request, 'edudealio/mcq.html', context)
    elif request.method == "POST":
        points = request.POST.get('points')
        user = request.user
        selected_class = request.session['selected_class']
        selected_topic = request.session['selected_topic']
        class_instance = ClassModel.objects.get(name=selected_class)
        topic_instance = AITopicModel.objects.get(name=selected_topic)
        questionnaire_model = QuestionnaireModel.objects.create(
            user=user,
            question_class=class_instance,
            topic=topic_instance,
            points=points)
        questionnaire_model.save()
        updatePoints(request, request.user, points)
        # Respond with a JSON response
        response_data = {'message': 'Points received successfully'}
        return JsonResponse(response_data)


class SupportView(View):
    def get(self, request):
        return render(request, "edudealio/support.html")

    def post(self, request):
        try:
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            contact_message = ContactMessageModel.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message)
            contact_message.save()
            send_message_successful_email(email, name, message)
            return JsonResponse({'status': 'success'})
        except Exception:
            return JsonResponse({'status': 'error'})


class AboutView(TemplateView):
    template_name = "edudealio/about.html"


@login_required(login_url='login')
def add_curriculum(request):
    if request.method == 'POST':
        form = StudentCurriculumForm(request.POST, request.FILES)
        if form.is_valid():
            curriculum = form.save(commit=False)
            if str(curriculum.activity) == 'other':
                new_activity_name = form.cleaned_data.get('new_activity')
                if new_activity_name:
                    try:
                        new_activity = ActivityModel.objects.get(
                            name=new_activity_name)
                    except ActivityModel.DoesNotExist:
                        new_activity = ActivityModel.objects.create(
                            name=new_activity_name)
                        curriculum.activity = new_activity
                    else:
                        return JsonResponse({'status': 'error', 'message': "Your activity name is in the available options."})
            curriculum.user = request.user
            curriculum.save()
            points = 20
            updatePoints(request, request.user, points)
            return JsonResponse({'status': 'success', 'message': "Score Uploaded successfully!"})
        else:
            return JsonResponse({'status': 'error', 'message': "Error in uploading the score."})
    else:
        form = StudentCurriculumForm()
    return render(request, 'edudealio/student_curriculum.html', {'form': form})


@login_required(login_url='login')
def add_standardize_test_score(request):
    if request.method == 'POST':
        form = StandardizeTestForm(request.POST, request.FILES)
        if form.is_valid():
            standardize_test = form.save(commit=False)
            if str(standardize_test.test_name) == 'other':
                add_test_name = form.cleaned_data.get('add_test_name')
                if add_test_name:
                    try:
                        new_test_name = StandardizeTestModel.objects.get(
                            name=add_test_name)
                    except StandardizeTestModel.DoesNotExist:
                        new_test_name = StandardizeTestModel.objects.create(
                            name=add_test_name)
                        standardize_test.test_name = new_test_name
                    else:
                        return JsonResponse({'status': 'error', 'message': "Your test name is in the available options."})
            standardize_test.user = request.user
            standardize_test.save()
            points = 20
            updatePoints(request, request.user, points)
            return JsonResponse({'status': 'success', 'message': "Score Uploaded successfully!"})
        else:
            return JsonResponse({'status': 'error', 'message': "Error in uploading the score."})
    else:
        form = StandardizeTestForm()
    return render(request, 'edudealio/standardize_test.html', {'form': form})


@login_required(login_url='login')
def share_link(request):
    """Create a view to generate shareable links"""
    referral_object = ReferralModel.objects.filter(user=request.user).first()
    if referral_object:
        referral_code = referral_object.referral_code
    else:
        refer_code = ReferralModel.objects.create(user=request.user)
        refer_code.save()   
        referral_code = refer_code.referral_code
    share_url = request.build_absolute_uri(
        reverse('register') + f'?ref={referral_code}'
    )  # Build URL
    return render(request, 'edudealio/refer_share.html', {'share_url': share_url})


# @user_passes_test(is_admin)
# def techuploaddataview(request):
#     return render(request,'edudealio/uploaddata.html')
