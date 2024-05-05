# Import necessary libraries
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserResponse
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

# Global variable to store accuracy
model_accuracy = None

# View to load and render the initial page
def start(request):
    try:
        user_response = UserResponse.objects.get(user=request.user)
        recommended_stream = user_response.recommended_stream
        return render(request, 'retake.html', {'recommended_stream': recommended_stream})
    except UserResponse.DoesNotExist:
        # If the user has not attended the quiz before, render the original start.html template
        return render(request, 'start.html')

# View to render the questionnaire page
def questionnaire_view(request):
    return render(request, 'questionnaire.html')

# Function to load the Random Forest model
def load_model():
    global model_accuracy  # Access the global accuracy variable
    np.random.seed(0)
    n_samples = 100000
    data = {
        'Mathematics': np.random.randint(1, 11, n_samples),
        'Physics': np.random.randint(1, 11, n_samples),
        'Chemistry': np.random.randint(1, 11, n_samples),
        'Biology': np.random.randint(1, 11, n_samples),
        'Computer_Science': np.random.randint(1, 11, n_samples),
        'Accountancy': np.random.randint(1, 11, n_samples),
        'Business_Studies': np.random.randint(1, 11, n_samples),
        'Economics': np.random.randint(1, 11, n_samples),
        'History': np.random.randint(1, 11, n_samples),
        'Geography': np.random.randint(1, 11, n_samples),
        'Political_Science': np.random.randint(1, 11, n_samples),
        'Psychology': np.random.randint(1, 11, n_samples),
        'Sociology': np.random.randint(1, 11, n_samples),
        'Philosophy': np.random.randint(1, 11, n_samples),
        'Languages': np.random.randint(1, 11, n_samples)
    }
    data_df = pd.DataFrame(data)

    def calculate_stream(row):
        science_score = np.mean([row['Mathematics'], row['Physics'], row['Chemistry'], row['Biology'], row['Computer_Science']])
        commerce_score = np.mean([row['Mathematics'], row['Accountancy'], row['Business_Studies'], row['Economics']])
        arts_score = np.mean([row['History'], row['Geography'], row['Political_Science'], row['Economics'],
                            row['Psychology'], row['Sociology'], row['Philosophy'], row['Languages']])
        scores = {'Science': science_score, 'Commerce': commerce_score, 'Arts': arts_score}
        max_score = max(scores.values())
        recommended_streams = [stream for stream, score in scores.items() if score == max_score]
        return recommended_streams[0]

    labels_df = data_df.apply(calculate_stream, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(data_df, labels_df, test_size=0.3, random_state=42)

    clf_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_rf.fit(X_train, y_train)
    y_pred_rf = clf_rf.predict(X_test)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    model_accuracy = accuracy_rf* 100 # Store accuracy globally
    print(f"Random Forest Accuracy: {accuracy_rf * 100:.2f}%")

    # Cross-Validation Accuracy
    cv_scores_rf = cross_val_score(clf_rf, data_df, labels_df, cv=5)
    print(f"Random Forest CV Accuracy: {np.mean(cv_scores_rf) * 100:.2f}%")

    return clf_rf

# Load the model only once when the module is loaded
loaded_model = load_model()

# Function to predict stream based on user responses
def predict_stream(request):
    if request.method == 'POST':
        # Extract scores from POST data
        math_score = request.POST.get('knob1_score')
        physics_score = request.POST.get('knob2_score')
        chemistry_score = request.POST.get('knob3_score')
        biology_score = request.POST.get('knob4_score')
        computer_science_score = request.POST.get('knob5_score')
        accountancy_score = request.POST.get('knob6_score')
        business_studies_score = request.POST.get('knob7_score')
        economics_score = request.POST.get('knob8_score')
        history_score = request.POST.get('knob9_score')
        geography_score = request.POST.get('knob10_score')
        political_science_score = request.POST.get('knob11_score')
        psychology_score = request.POST.get('knob12_score')
        sociology_score = request.POST.get('knob13_score')
        philosophy_score = request.POST.get('knob14_score')
        languages_score = request.POST.get('knob15_score')

        # Check if any score is None
        if None in [math_score, physics_score, chemistry_score, biology_score, computer_science_score,
                    accountancy_score, business_studies_score, economics_score, history_score,
                    geography_score, political_science_score, psychology_score, sociology_score,
                    philosophy_score, languages_score]:
            # Handle the case where a score is missing
            return JsonResponse({'error': 'One or more scores are missing'})

        # Convert scores to integers
        math_score = int(math_score)
        physics_score = int(physics_score)
        chemistry_score = int(chemistry_score)
        biology_score = int(biology_score)
        computer_science_score = int(computer_science_score)
        accountancy_score = int(accountancy_score)
        business_studies_score = int(business_studies_score)
        economics_score = int(economics_score)
        history_score = int(history_score)
        geography_score = int(geography_score)
        political_science_score = int(political_science_score)
        psychology_score = int(psychology_score)
        sociology_score = int(sociology_score)
        philosophy_score = int(philosophy_score)
        languages_score = int(languages_score)

        # Process user responses
        user_responses = np.array([[
            math_score, physics_score, chemistry_score, biology_score, computer_science_score,
            accountancy_score, business_studies_score, economics_score, history_score,
            geography_score, political_science_score, psychology_score, sociology_score,
            philosophy_score, languages_score
        ]])

        # Predict the stream
        stream = loaded_model.predict(user_responses)[0]

        # Get the current user
        user = request.user

        # Check if the user has already attended the quiz
        user_response, created = UserResponse.objects.get_or_create(user=user)

        # Update the quiz scores and recommended stream
        user_response.math_score = math_score
        user_response.physics_score = physics_score
        user_response.chemistry_score = chemistry_score
        user_response.biology_score = biology_score
        user_response.computer_science_score = computer_science_score
        user_response.accountancy_score = accountancy_score
        user_response.business_studies_score = business_studies_score
        user_response.economics_score = economics_score
        user_response.history_score = history_score
        user_response.geography_score = geography_score
        user_response.political_science_score = political_science_score
        user_response.psychology_score = psychology_score
        user_response.sociology_score = sociology_score
        user_response.philosophy_score = philosophy_score
        user_response.languages_score = languages_score
        user_response.recommended_stream = stream
        user_response.save()

        # Redirect to the result page
        return redirect('result', recommended_stream=stream)

    # Render the questionnaire page
    return render(request, 'questionnaire.html')

# View to render the result page
def result(request, recommended_stream):
    global model_accuracy  # Access the global accuracy variable
    disclaimer_message = "Disclaimer: The recommended stream is based on predictive modeling and should be used as a general guideline. Individual preferences, aptitudes, and circumstances may vary. It is advisable to seek guidance from a career counselor or educational advisor for personalized advice."
    return render(request, 'result.html', {'recommended_stream': recommended_stream, 'accuracy': model_accuracy, 'disclaimer_message': disclaimer_message})
