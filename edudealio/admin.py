from django.contrib import admin
from .models import *


# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    """Represent subscription model on admin page"""
    list_display = ("email","date")

class StudentPointsAdmin(admin.ModelAdmin):
    """Represent name,date, and points on admin page"""
    list_display = ("user","points","date")

class QuestionnaireAdmin(admin.ModelAdmin):
    """Represent user, class, topic, date on admin page"""
    list_display = ("user","question_class","topic","date")

class ActivityAdmin(admin.ModelAdmin):
    """Represent the activity name"""
    list_display = ("name",)
    
class StudentSubjectAdmin(admin.ModelAdmin):
    """Represent the student, subject and percentage"""
    list_display = ("student", "subject", "percentage", "student_class", "semester")

admin.site.register(SubscriptionModel,SubscriptionAdmin)
admin.site.register(SchoolModel)
admin.site.register(ClassModel)
admin.site.register(SubjectModel)
admin.site.register(StudentModel)
admin.site.register(StudentSubjectModel, StudentSubjectAdmin)
admin.site.register(OffersModel)
admin.site.register(StudentAvailOffersModel)
admin.site.register(StudentDashboardDataModel)
admin.site.register(StudentPointsModel,StudentPointsAdmin)
admin.site.register(CouponCodeModel)
admin.site.register(QuestionnaireModel,QuestionnaireAdmin)
admin.site.register(ContactMessageModel)
admin.site.register(StudentCurriculumModel)
admin.site.register(ActivityModel,ActivityAdmin)
admin.site.register(StandardizeTestAchievementModel)
admin.site.register(StandardizeTestModel)
admin.site.register(ReferralModel)
admin.site.register(UserProfileModel)
admin.site.register(AITopicModel)