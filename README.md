# Google Drive File Translator
=============================

A Python app that translates files from one language to another using the OpenAI API and Google Drive API.

## Getting Started

### Prerequisites

* Python 3.9+
* OpenAI API key
* Google Drive API credentials
* Docker (optional)

### Installation

1. Clone the repository: `git clone https://github.com/BigFatherJesus/AGDT.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your OpenAI API key and Google Drive API credentials:
OPENAI_API_KEY=your_openai_api_key GOOGLE_DRIVE_CREDENTIALS=your_google_drive_credentials INPUT_FOLDER_ID=your_input_folder_id OUTPUT_FOLDER_ID=your_output_folder_id

4. Run the app: `python main.py`

### Dockerization

1. Build the Docker image: `docker build -t google-drive-file-translator .`
2. Run the Docker container: `docker run -p 8080:8080 google-drive-file-translator`

## Usage

The app will automatically translate files from the input folder to the output folder using the OpenAI API. The translated files will have the same name as the original file but with a `_translated` suffix.

## Configuration

You can configure the app by setting the following environment variables:

* `INPUT_FOLDER_ID`: The ID of the Google Drive folder containing the files to be translated.
* `OUTPUT_FOLDER_ID`: The ID of the Google Drive folder where the translated files will be saved.
* `OPENAI_API_KEY`: Your OpenAI API key.
* `GOOGLE_DRIVE_CREDENTIALS`: Your Google Drive API credentials.

## Contributing

Contributions are welcome! Please open a pull request to contribute to the app.

