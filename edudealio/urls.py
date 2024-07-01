from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from django.views.generic.base import RedirectView
# from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),

    path("login", views.loginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("verify", views.VerifyView.as_view(), name="verify"),
    path("logout", views.logoutpage, name="logout"),
    path("subscribe", views.SubscribeMemberView.as_view(), name="subscribe"),

    path("uploadmarks", views.uploadmarksview, name="uploadmarks"),
    path("curriculum", views.add_curriculum, name="curriculum"),
    path("standardize-test", views.add_standardize_test_score,
         name="standardize-test"),

    path("dashboard", views.dashboardview, name="dashboard"),

    path("questionnaire", views.questionnaireview, name="questionnaire"),
    path("uploaddata", views.uploadmarksview, name="uploaddata"),
    path("mcqdata", views.mcqview, name="mcq"),

    path("support", views.SupportView.as_view(), name="support"),
    path("about", views.AboutView.as_view(), name="about"),
    path("refer", views.share_link, name="refer"),

    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="edudealio/reset_password.html"
        ),
        name="password_reset"),

    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="edudealio/reset_email_sent.html"
        ),
        name="password_reset_done"),

    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="edudealio/reset_password_confirm.html"
        ),
        name="password_reset_confirm"),

    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="edudealio/reset_password_done.html"
        ),
        name="password_reset_complete"),
]


# path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
