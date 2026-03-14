from utils.url_extractor import URLExtractor

message = "Verify your account here https://fake-bank-login.com immediately"

urls = URLExtractor.extract_urls(message)

print(urls)