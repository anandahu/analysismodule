<<<<<<< HEAD
# analysisoutput

This project is a Django-based web application designed for sentiment analysis of uploaded CSV files. The application allows users to sign up, log in, upload files, select columns for analysis, and view the results in various visual formats.

## Project Structure

### 1. `views.py`

This file contains the views for handling user interactions and processing data.

- **Imports**: Includes necessary Django modules, models, forms, and external libraries for data processing and visualization.
- **SignUpView**: Handles user registration using a custom signup form.
- **FileUploadView**: Manages file uploads, associates files with the logged-in user, and triggers the cleaning process.
- **FileListView**: Displays a list of files uploaded by the current user.
- **process_file**: Processes the uploaded file for sentiment analysis, generates visualizations, and renders the results page.
- **clean_csv**: Cleans the uploaded CSV file by removing rows with missing values.

### 2. `settings.py`

This file contains the configuration settings for the Django project.

- **BASE_DIR**: Defines the base directory of the project.
- **SECRET_KEY**: Secret key for the Django application.
- **DEBUG**: Debug mode setting.
- **ALLOWED_HOSTS**: List of allowed hosts.
- **INSTALLED_APPS**: List of installed applications, including the custom `output` app.
- **AUTH_USER_MODEL**: Specifies the user model to use.
- **LOGIN_REDIRECT_URL**: URL to redirect to after login.
- **LOGIN_URL**: URL for the login page.
- **MEDIA_URL**: URL for serving media files.
- **MEDIA_ROOT**: Directory for storing media files.
- **MIDDLEWARE**: List of middleware components.
- **ROOT_URLCONF**: Root URL configuration.
- **TEMPLATES**: Template settings.
- **WSGI_APPLICATION**: WSGI application configuration.
- **DATABASES**: Database configuration (SQLite).
- **AUTH_PASSWORD_VALIDATORS**: Password validation settings.
- **LANGUAGE_CODE**: Language code setting.
- **TIME_ZONE**: Time zone setting.
- **USE_I18N**: Internationalization setting.
- **USE_TZ**: Time zone setting.
- **STATIC_URL**: URL for serving static files.
- **DEFAULT_AUTO_FIELD**: Default primary key field type.

### 3. `forms.py`

This file contains the forms used in the application.

- **SignUpForm**: Custom user registration form based on Django's built-in `UserCreationForm`.
- **FileUploadForm**: Form for uploading files, based on Django's `ModelForm`.

### 4. `models.py`

This file defines the database models for the application.

- **UserFile**: Model representing a file uploaded by a user. It includes fields for the user, file, upload timestamp, and cleaned file.

### 5. `urls.py`

This file defines the URL patterns for the `output` app.

- **signup**: URL for user signup.
- **login**: URL for user login.
- **logout**: URL for user logout.
- **upload**: URL for file uploads.
- **file_list**: URL for listing uploaded files.
- **process**: URL for processing a file.

### 6. `urls.py` (Project-level)

This file defines the URL patterns for the entire project.

- **RedirectView**: Redirects the root URL to the login page.
- **signup**: URL for user signup.
- **login**: URL for user login.
- **logout**: URL for user logout.
- **upload**: URL for file uploads.
- **file_list**: URL for listing uploaded files.
- **process**: URL for processing a file.
- **admin**: URL for the Django admin interface.
- **files**: Includes the URL patterns from the `output` app.
- **static**: Serves media files during development.

### 7. Templates

#### `signup.html`

Template for the user signup page.

- **Form**: Displays the signup form and a submit button.

#### `login.html`

Template for the user login page.

- **Form**: Displays the login form and a submit button.
- **Link**: Provides a link to the signup page.

#### `list.html`

Template for displaying the list of uploaded files.

- **File List**: Displays the list of files uploaded by the user with options to process each file.
- **Upload Link**: Provides a link to the file upload page.
- **Logout Form**: Provides a logout button.

#### `upload.html`

Template for the file upload page.

- **Form**: Displays the file upload form and a submit button.
- **View Files Link**: Provides a link to the file list page.
- **Logout Form**: Provides a logout button.

#### `select_columns.html`

Template for selecting columns for sentiment analysis.

- **Form**: Displays a list of columns with checkboxes for selection and a submit button.
- **Logout Form**: Provides a logout button.

#### `results.html`

Template for displaying the results of sentiment analysis.

- **Results Table**: Displays the sentiment analysis results in a table format.
- **Charts**: Displays various charts generated using Plotly.
- **Back Link**: Provides a link to the file list page.
- **Logout Form**: Provides a logout button.

## How to Run the Project


