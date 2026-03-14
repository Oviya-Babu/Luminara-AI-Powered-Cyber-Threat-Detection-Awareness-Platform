from services.phishing.phishing_classifier import PhishingClassifier

classifier = PhishingClassifier()

message = "Your account has been suspended. Verify immediately."

result = classifier.predict(message)

print(result)