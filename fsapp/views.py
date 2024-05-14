import csv
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import Feedback
from transformers import pipeline
from io import TextIOWrapper  
from .utils import get_amazon_product_info, save_product_info_to_csv
from django.contrib import messages

def amazon_reviews(request):
    if request.method == 'POST':
        amazon_url = request.POST.get('amazon_url')
        if amazon_url:
            product_name, product_image, reviews = get_amazon_product_info(amazon_url)
            if product_name and product_image and reviews:
                save_product_info_to_csv(product_name, product_image, reviews, 'amazon_reviews.csv')
                return render(request, 'amazon_reviews_success.html', {'filename': 'amazon_reviews.csv'})
            else:
                return render(request, 'amazon_reviews_failure.html')
        else:
            return HttpResponseBadRequest("Amazon URL is required")
    return render(request, 'amazon_reviews.html')

def analysis(request):
    if request.method == 'POST':
        review = request.POST.get('review_text')
        sent_pipeline = pipeline("sentiment-analysis")
        sentiment = sent_pipeline(review)[0]
        return render(request, 'results.html', {'review_text': review, 'sentiment': sentiment})
    else:
        return render(request, 'analysis.html')

def bulkreview(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, "No file uploaded", extra_tags='error')
            return render(request, 'bulkreview.html')

        # Get the uploaded CSV file
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Uploaded file is not a CSV", extra_tags='error')
            return render(request, 'bulkreview.html')

        # Initialize sentiment analysis pipeline
        sent_pipeline = pipeline("sentiment-analysis")

        # Process the CSV file
        reviews = []
        positive_reviews = 0
        negative_reviews = 0
        product_name = None
        product_image = None

        # Parse the CSV file
        csv_text = TextIOWrapper(csv_file.file, encoding=request.encoding)
        csv_reader = csv.DictReader(csv_text)

        for row in csv_reader:
            review_text = row.get('Review')

            # Extract product name and image URL
            if not product_name:
                product_name = row.get('Product Name')
            if not product_image:
                product_image = row.get('Product Image')

            # Skip empty review texts
            if not review_text:
                continue

            sentiment = sent_pipeline(review_text)[0]

            reviews.append((review_text, sentiment))

            # Count positive and negative reviews
            if sentiment['label'] == 'POSITIVE':
                positive_reviews += 1
            elif sentiment['label'] == 'NEGATIVE':
                negative_reviews += 1

        # Calculate general sentiment
        total_reviews = len(reviews)
        general_sentiment = "POSITIVE" if positive_reviews > negative_reviews else "NEGATIVE"

        # Render bulkanalysis.html with the results
        return render(request, 'bulkanalysis.html', {
            'reviews': reviews,
            'total_reviews': total_reviews,
            'positive_reviews': positive_reviews,
            'negative_reviews': negative_reviews,
            'general_sentiment': general_sentiment,
            'product_name': product_name,
            'product_image': product_image
        })
    else:
        return render(request, 'bulkreview.html')

def send_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        feedback = Feedback.objects.create(name=name, email=email, message=message)
        feedback.save()
        return render(request, 'feedback_success.html')  # Render a success template
    return render(request, 'contact_form.html')

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")
