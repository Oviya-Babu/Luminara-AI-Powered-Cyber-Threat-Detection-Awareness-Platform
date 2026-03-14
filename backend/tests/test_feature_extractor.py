from services.phishing.feature_extractor import FeatureExtractor

extractor = FeatureExtractor()

message = "Your bank account is locked. Verify immediately here https://secure-login-bank.xyz"

features = extractor.extract_features(message)

print(features)