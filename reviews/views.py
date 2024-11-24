from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render
from .models import Product

# Landing Page
def index(request):
    # Fetch all products
    products = Product.objects.all()

    # Handle search functionality
    search_query = request.GET.get('search', '')  # Get search term from query parameters
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    return render(request, 'index.html', {'products': products, 'search_query': search_query})


# User Registration
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    return render(request, 'register.html')

# User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# User Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

from .models import Product  # Import the Product model

# Dashboard (Requires Login)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, Review
from django.db.models import Avg

@login_required
def dashboard(request):
    # Fetch all products from the Product model, and calculate the average sentiment score
    products = Product.objects.all()

    # Calculate the average sentiment score for each product based on reviews
    for product in products:
        # Get the sentiment scores of all reviews for the current product
        reviews = Review.objects.filter(product=product)

        # Calculate the average sentiment score (if there are reviews)
        if reviews.exists():
            avg_sentiment = reviews.aggregate(Avg('sentiment_score'))['sentiment_score__avg']
            product.avg_sentiment_score = avg_sentiment
        else:
            product.avg_sentiment_score = 0  # No reviews yet, set to neutral

    # Sort products based on the average sentiment score (higher scores come first)
    sorted_products = sorted(products, key=lambda p: p.avg_sentiment_score, reverse=True)

    return render(request, 'dashboard.html', {'products': sorted_products})




from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Review
import re
import nltk
from nltk.corpus import stopwords

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Download NLTK stopwords (if not already downloaded)
# nltk.download('stopwords')

# Preprocess the review text
def preprocess_review(review_text):
    # Convert text to lowercase
    review_text = review_text.lower()
    
    # Remove punctuation and special characters
    review_text = re.sub(r'[^\w\s]', '', review_text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    review_text = ' '.join([word for word in review_text.split() if word not in stop_words])
    
    return review_text

# Add Review View
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if user has already reviewed this product
    if Review.objects.filter(user=request.user, product=product).exists():
        # Allow users to post multiple reviews (no restriction on count)
        pass

    if request.method == "POST":
        review_text = request.POST['review_text']
        
        # Preprocess the review text before sentiment analysis
        processed_text = preprocess_review(review_text)
        
        # Perform sentiment analysis using VADER
        sentiment_scores = analyzer.polarity_scores(processed_text)
        sentiment_score = sentiment_scores['compound']
        
        # Determine the sentiment label based on the score
        if sentiment_score > 0:
            sentiment_label = 'positive'
        elif sentiment_score < 0:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        
        ip_address = request.META.get('REMOTE_ADDR')  # Get the IP address of the user
        
        # Create and save the review
        review = Review.objects.create(
            product=product,
            user=request.user,
            review_text=review_text,
            ip_address=ip_address,
            sentiment_label=sentiment_label,
            sentiment_score=sentiment_score,
        )
        
        # Check if the review is fake (based on repeated IP addresses)
        review_count_from_ip = Review.objects.filter(ip_address=ip_address, product=product).count()
        if review_count_from_ip > 2:  # Example condition to flag fake review
            review.is_fake = True
            review.save()
            messages.warning(request, "This review has been flagged as fake due to multiple reviews from the same IP address.")
        else:
            messages.success(request, "Your review has been posted successfully.")
        
        return redirect('dashboard')
    
    return render(request, 'add_review.html', {'product': product})
