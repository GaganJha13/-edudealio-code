from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from edudealio.models import StudentPointsModel, StudentDashboardDataModel  # Import your UserPoints model
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):
    help = 'Collect points from users'

    def add_points(self):
            users = User.objects.all()
            today = date.today()
            # Iterate through users and update points
            for user in users:
                if user.username != "admin":
                    # Get or create the UserPoints instance for the user
                    user_points = StudentDashboardDataModel.objects.get(user=user).active_points
                    try:
                        user_active_points_today = StudentPointsModel.objects.get(user=user,points=user_points,date=today)
                    except StudentPointsModel.DoesNotExist:
                        user_active_point_update = StudentPointsModel.objects.create(user=user,points=user_points,date=today)
                        user_active_point_update.save()
            self.stdout.write(self.style.SUCCESS('Custom command executed successfully.'))

    def handle(self, *args, **options):
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.add_points, 'interval', seconds=10)
        scheduler.start()
        # Ensure the scheduler keeps running after the management command exits
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()