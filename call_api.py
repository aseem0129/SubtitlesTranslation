import requests

# Your API endpoint
url = 'http://127.0.0.1:5000/translate_srt'

# Prompt the user to input the SRT file path and target language
srt_file_path = input("Enter the path to your SRT file (e.g., C:/Users/aseem/Downloads/movie.srt): ")
target_language = input("Enter the target language (e.g., 'es' for Spanish, 'fr' for French): ")

# Open the SRT file in binary mode and prepare to send the request
try:
    with open(srt_file_path, 'rb') as srt_file:
        response = requests.post(url, files={'srt_file': srt_file}, data={'target_language': target_language})

    # Check if the request was successful
    if response.status_code == 200:
        # Save the translated SRT file locally
        output_file_path = 'translated_subtitles.srt'
        with open(output_file_path, 'wb') as output_file:
            output_file.write(response.content)
        print(f"Translated SRT file saved as {output_file_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except FileNotFoundError:
    print(f"Error: The file at {srt_file_path} was not found.")
