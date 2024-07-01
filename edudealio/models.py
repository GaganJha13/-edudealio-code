"""To build models using parent models library"""
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .utils import generate_referral_code

# Create your models here.


class SubscriptionModel(models.Model):
    """A model for containing subscribers"""
    email = models.EmailField(max_length=254, unique=True)
    date = models.DateField(auto_now=True)


class SchoolModel(models.Model):
    """Model to collect school names"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class ClassModel(models.Model):
    """Model to collect class name"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class SubjectModel(models.Model):
    """Model to collect subject name"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class StudentModel(models.Model):
    """Model to collect data of academic marks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10)
    semester = models.CharField(max_length=20)
    school = models.ForeignKey(SchoolModel, on_delete=models.CASCADE)
    custom_school_name = models.CharField(
        max_length=100, blank=True, null=True)
    student_class = models.ForeignKey(ClassModel, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(
        SubjectModel, through='StudentSubjectModel')
    exam_certificate = models.FileField(upload_to='academic/')

    def __str__(self):
        return str(self.user.username)


class StudentSubjectModel(models.Model):
    """Model to collect student subject name and percentage in the same."""
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                     MinValueValidator(0.01)])
    student_class = models.ForeignKey(
        ClassModel, on_delete=models.CASCADE, null=True)
    semester = models.CharField(max_length=20, null=True)
    added_on = models.DateField(auto_now=True, null=True)

    class Meta:
        """Unique student and subject data for each academic score model"""
        unique_together = ['student', 'subject']


class OffersModel(models.Model):
    """Model to collect offer data"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    brand = models.CharField(max_length=100)
    img_url = models.CharField(max_length=500, null=True, blank=True)
    tags = TaggableManager()
    validity_period = models.DateField()

    def __str__(self):
        return str(self.title)


class StudentDashboardDataModel(models.Model):
    """collect user points and uploads data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    active_points = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    uploads = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    offers_avail = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])


class StudentAvailOffersModel(models.Model):
    """Collect offers and date of offers avail data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offers = models.ForeignKey(OffersModel, on_delete=models.CASCADE)
    date_offer_avail = models.DateField(auto_now=True)


class StudentPointsModel(models.Model):
    """Collect student active points with dates for graph"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user.username)


class CouponCodeModel(models.Model):
    """Collect coupon code avail and status by student"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offers = models.ForeignKey(OffersModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    redeemed = models.BooleanField(default=False)


class AITopicModel(models.Model):
    """Trained AI topics for quiz"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class QuestionnaireModel(models.Model):
    """Collect question subject and points from questionnaire"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_class = models.ForeignKey(ClassModel, on_delete=models.CASCADE)
    topic = models.ForeignKey(AITopicModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    points = models.PositiveIntegerField(validators=[MinValueValidator(0)])


class ContactMessageModel(models.Model):
    """Collect messages data from support page"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ActivityModel(models.Model):
    """Collect activity name from student curriculum achievement"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class StudentCurriculumModel(models.Model):
    """Model to collect curriculum achievement detail of student"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityModel, on_delete=models.CASCADE)
    description = models.TextField()
    certificate = models.FileField(upload_to='curriculum/')

    def __str__(self):
        return str(self.user.username)


class StandardizeTestModel(models.Model):
    """Model to collect the name of standardize test"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class StandardizeTestAchievementModel(models.Model):
    """Model to collect data for standardize tests"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.ForeignKey(
        StandardizeTestModel, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[
        MinValueValidator(0.01)])
    certificate = models.FileField(upload_to='standardize/')


class ReferralModel(models.Model):
    """A model to associate suer with their referral code"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(
        max_length=8, unique=True, default=generate_referral_code)


class UserProfileModel(models.Model):
    """Keep track of fields related to the user's profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referred_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
