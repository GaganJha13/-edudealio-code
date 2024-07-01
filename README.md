EduDealio - Offer Platform
=========================

EduDealio is a web application built on Django that aims to provide exclusive offers to students based on their academic achievements and quiz performances.

Features
--------

- **Points-Based Rewards:** Students earn points based on their academic scores and quiz performance.
- **Personalized Offers:** Tailored offers are provided to students based on their accumulated points.
- **Academic Score Integration:** Academic scores contribute to a student's point accumulation.
- **Quiz Challenges:** Engaging quizzes enable students to earn additional points.
- **User Authentication:** Secure login and authentication system for students and administrators.
- **Admin Panel:** An admin panel to manage offers, user accounts, and points distribution.

Installation
------------

To run this application locally, follow these steps:

1. Clone this repository:

   ```sh

      git clone https://github.com/Scholarsphere-Ventures-Pvt-Ltd/web-app-django.git
   ```

2. Create a virtual environment (recommended):

   ```sh

      python -m venv env
   ```

3. Activate the virtual environment:

   - On Windows:

     ```sh

        .\env\Scripts\activate

   - On macOS and Linux:
      ```sh
  
          source env/bin/activate
      ```

4. Install dependencies:

   Install the required dependencies by running the following command:

   ```sh

      pip install -r requirements.txt

5. Include environment variables:

   * Create a `.env` file and add environment variables.
   * Install the `python-decouple` package:

     ```sh

        pip install python-decouple

   * Configure environment variables in `local.py`:

     For example:

     local.py

         from decouple import config

         SECRET_KEY = config('SECRET_KEY')

         DEBUG = config('DEBUG', default=False, cast=bool)
         # Add more environment variables as needed...
