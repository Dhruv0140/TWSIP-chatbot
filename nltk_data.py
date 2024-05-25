import nltk
nltk.download('vader_lexicon')

# Check if NLTK data files are available, if not, download them silently
nltk.download('punkt', download_dir='path_to_your_project_directory/nltk_data', quiet=True)
nltk.download('chat80', download_dir='path_to_your_project_directory/nltk_data', quiet=True)
nltk.download('vader_lexicon', download_dir='path_to_your_project_directory/nltk_data', quiet=True)

