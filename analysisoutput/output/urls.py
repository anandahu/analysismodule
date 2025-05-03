from django.urls import path
from .views import SignUpView, FileUploadView, FileListView, process_file, line_chart_view, bar_chart_view, pie_chart_view, scatter_plot_view, positive_words_chart_view, delete_file
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Add the logout view
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('', FileListView.as_view(), name='file_list'),
    path('process/<int:file_id>/', process_file, name='process'),
    path('line_chart/', line_chart_view, name='line_chart'),
    path('bar_chart/', bar_chart_view, name='bar_chart'),
    path('pie_chart/', pie_chart_view, name='pie_chart'),
    path('scatter_plot/', scatter_plot_view, name='scatter_plot'),
    path('positive_words_chart/', positive_words_chart_view, name='positive_words_chart'),
    path('delete_file/<int:file_id>/', delete_file, name='delete_file'),
]