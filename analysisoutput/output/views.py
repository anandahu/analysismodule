from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import UserFile
from .forms import SignUpForm, FileUploadForm
import pandas as pd
import os
from django.conf import settings
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
from django.http import HttpResponseRedirect
from django.urls import reverse

# User registration view
class SignUpView(CreateView):
    form_class = SignUpForm  # Uses a custom signup form
    template_name = 'registration/signup.html'  # Renders the signup page

    def form_valid(self, form):
        """Handles successful form submission by saving the user and logging them in."""
        user = form.save()
        login(self.request, user)
        return redirect('file_list')  # Redirects to the file list page after signup

# File upload view
class FileUploadView(LoginRequiredMixin, CreateView):
    model = UserFile
    form_class = FileUploadForm  # Uses a custom file upload form
    template_name = 'files/upload.html'  # Template for file upload page
    success_url = '/files/'  # Redirects to file list after upload

    def form_valid(self, form):
        """Handles file upload and triggers cleaning process."""
        form.instance.user = self.request.user  # Assign the uploaded file to the logged-in user
        response = super().form_valid(form)  # Save the uploaded file

        # Clean the uploaded CSV file
        cleaned_file_path = clean_csv(form.instance.file.path)
        form.instance.cleaned_file.name = cleaned_file_path  # Save cleaned file path in model
        form.instance.save()  # Save changes to the database

        return response  # Proceed with normal form submission flow

# File list view
class FileListView(LoginRequiredMixin, ListView):
    model = UserFile
    template_name = 'files/list.html'  # Template for displaying uploaded files
    context_object_name = 'files'  # Name used to access the files in the template

    def get_queryset(self):
        """Filters the file list to show only files uploaded by the current user."""
        return UserFile.objects.filter(user=self.request.user)

# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Initialize sentiment analysis and stop words
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

def remove_stop_words(text):
    """Removes stop words from the given text."""
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

@login_required
def process_file(request, file_id):
    try:
        file_obj = UserFile.objects.get(id=file_id, user=request.user)
        file_path = file_obj.cleaned_file.path if file_obj.cleaned_file else file_obj.file.path

        try:
            df = pd.read_csv(file_path)
        except pd.errors.ParserError as e:
            return render(request, 'files/error.html', {'error': f"Error reading CSV file: {e}"})

        column_list = df.columns.tolist()
        if request.method == 'POST':
            selected_columns = request.POST.getlist('columns')
            if not selected_columns:
                return render(request, 'files/select_columns.html', {'columns': column_list, 'error': "Please select at least one column."})

            sentiment_results = []
            word_corpus_high = []
            positive_reviews = []
            neutral_reviews = []
            negative_reviews = []

            for index, row in df.iterrows():
                text = ' '.join(str(row[col]) for col in selected_columns if pd.notna(row[col]))
                text = remove_stop_words(text)
                sentiment = sia.polarity_scores(text)
                sentiment_results.append({"text": text, "sentiment": sentiment})

                if sentiment['compound'] > 0.5:
                    word_corpus_high.extend(text.split())
                    positive_reviews.append(text)
                elif sentiment['compound'] < -0.5:
                    negative_reviews.append(text)
                else:
                    neutral_reviews.append(text)

            # Limit the text results shown to the first 10
            limited_sentiment_results = sentiment_results[:10]

            texts = [result['text'] for result in limited_sentiment_results]
            positives = [result['sentiment']['pos'] for result in limited_sentiment_results]
            neutrals = [result['sentiment']['neu'] for result in limited_sentiment_results]
            negatives = [result['sentiment']['neg'] for result in limited_sentiment_results]
            compounds = [result['sentiment']['compound'] for result in limited_sentiment_results]

            line_chart = go.Figure()
            line_chart.add_trace(go.Scatter(x=texts, y=compounds, mode='lines+markers', name='Compound', hoverinfo='x+y+text', text=texts))
            line_chart.update_layout(title="Line Chart", xaxis_tickangle=-45, template="ggplot2", width=1000, height=600)
            request.session['line_chart_html'] = line_chart.to_html(full_html=False)

            bar_chart = go.Figure()
            bar_chart.add_trace(go.Bar(x=texts, y=positives, name='Positive', hoverinfo='x+y+text', text=texts))
            bar_chart.add_trace(go.Bar(x=texts, y=neutrals, name='Neutral', hoverinfo='x+y+text', text=texts))
            bar_chart.add_trace(go.Bar(x=texts, y=negatives, name='Negative', hoverinfo='x+y+text', text=texts))
            bar_chart.update_layout(title="Bar Chart", xaxis_tickangle=-45, template="ggplot2", width=1000, height=600)
            request.session['bar_chart_html'] = bar_chart.to_html(full_html=False)

            pie_chart = go.Figure()
            pie_chart.add_trace(go.Pie(labels=['Positive', 'Neutral', 'Negative'], values=[sum(positives), sum(neutrals), sum(negatives)], hoverinfo='label+percent+value'))
            pie_chart.update_layout(title="Pie Chart", template="ggplot2", width=10000, height=6000)
            request.session['pie_chart_html'] = pie_chart.to_html(full_html=False)

            scatter_plot = go.Figure()
            scatter_plot.add_trace(go.Scatter(x=texts, y=compounds, mode='markers', name='Compound', hoverinfo='x+y+text', text=texts))
            scatter_plot.update_layout(title="Scatter Plot", xaxis_tickangle=-45, template="ggplot2", width=1000, height=600)
            request.session['scatter_plot_html'] = scatter_plot.to_html(full_html=False)

            positives_df = pd.DataFrame(Counter(word_corpus_high).most_common(20), columns=['word', 'frequency'])
            positive_words_chart = px.bar(positives_df, x='word', y='frequency', title='Most frequent words in Positive Reviews', template="ggplot2", width=1000, height=600)
            request.session['positive_words_chart_html'] = positive_words_chart.to_html(full_html=False)

            # Add the number of reviews used for the analysis to the session
            request.session['num_reviews'] = len(sentiment_results)
            request.session['total_reviews'] = len(df)  # Add the total number of reviews to the session

            return redirect('line_chart')

        return render(request, 'files/select_columns.html', {'columns': column_list})

    except UserFile.DoesNotExist:
        return redirect('file_list')

def clean_csv(file_path):
    """Cleans the CSV file by removing rows with missing values."""
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna()  # Remove empty rows
    cleaned_file_path = os.path.join(settings.MEDIA_ROOT, 'cleaned', os.path.basename(file_path))
    df_cleaned.to_csv(cleaned_file_path, index=False)  # Save cleaned CSV file
    return cleaned_file_path  # Return cleaned file path

@login_required
def delete_file(request, file_id):
    """Handles the deletion of an uploaded file."""
    try:
        file_obj = UserFile.objects.get(id=file_id, user=request.user)
        original_file_path = file_obj.file.path
        cleaned_file_path = file_obj.cleaned_file.path if file_obj.cleaned_file else None

        # Delete the file object from the database
        file_obj.delete()

        # Delete the original file from the filesystem
        if os.path.exists(original_file_path):
            os.remove(original_file_path)

        # Delete the cleaned file from the filesystem
        if cleaned_file_path and os.path.exists(cleaned_file_path):
            os.remove(cleaned_file_path)

        return HttpResponseRedirect(reverse('file_list'))
    except UserFile.DoesNotExist:
        return redirect('file_list')

@login_required
def line_chart_view(request):
    return render(request, 'files/line_chart.html', {
        'line_chart_html': request.session.get('line_chart_html'),
        'num_reviews': request.session.get('num_reviews')
    })

@login_required
def bar_chart_view(request):
    return render(request, 'files/bar_chart.html', {
        'bar_chart_html': request.session.get('bar_chart_html'),
        'num_reviews': request.session.get('num_reviews'),
        'total_reviews': request.session.get('total_reviews')
    })

@login_required
def pie_chart_view(request):
    return render(request, 'files/pie_chart.html', {
        'pie_chart_html': request.session.get('pie_chart_html'),
        'num_reviews': request.session.get('num_reviews'),
        'total_reviews': request.session.get('total_reviews')
    })

@login_required
def scatter_plot_view(request):
    return render(request, 'files/scatter_plot.html', {
        'scatter_plot_html': request.session.get('scatter_plot_html'),
        'num_reviews': request.session.get('num_reviews'),
        'total_reviews': request.session.get('total_reviews')
    })

@login_required
def positive_words_chart_view(request):
    return render(request, 'files/positive_words_chart.html', {
        'positive_words_chart_html': request.session.get('positive_words_chart_html'),
        'num_reviews': request.session.get('num_reviews'),
        'total_reviews': request.session.get('total_reviews')
    })
