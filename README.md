
# Google Drive File Translator

This project is a Python script that translates files from one language to another using the OpenAI API and Google Drive API. It automates the translation of files in a Google Drive folder.

## Requirements

* Python 3.7+
* OpenAI API key
* Google Drive API credentials
* Docker (optional)

## Setup

### 1. Create a `.env` file

Create a `.env` file in the root of the project with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
INPUT_FOLDER_ID=your_input_folder_id
OUTPUT_FOLDER_ID=your_output_folder_id
SERVICE_ACCOUNT_FILE=credentials.json
OUTPUT_LANGUAGE=desired_language
```

**Replace the placeholders:**

* `your_openai_api_key`: Your actual OpenAI API key.
* `your_input_folder_id`: ID of the input folder in Google Drive.
* `your_output_folder_id`: ID of the output folder in Google Drive.
* `credentials.json`: Path to your Google Drive API credentials file.
* `desired_language`: The full name of the language you want the files to be translated to.

### 2. Install dependencies

Run the following command to install the required dependencies:

```
pip install -r requirements.txt
```

### 3. Run the script

Run the script using the following command:

```
python main.py
```

The script will start translating files in the input folder and upload the translated files to the output folder.

## Dockerization

To dockerize the script, follow these steps:

### 1. Create a Dockerfile

Create a Dockerfile in the root of the project with the following contents:

```
FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 2. Build the Docker image

Run the following command to build the Docker image:

```
docker build -t google-drive-file-translator .
```

### 3. Run the Docker container

Run the following command to run the Docker container:

```
docker run -e OPENAI_API_KEY=your_openai_api_key -e INPUT_FOLDER_ID=your_input_folder_id -e OUTPUT_FOLDER_ID=your_output_folder_id -e SERVICE_ACCOUNT_FILE=credentials.json -e OUTPUT_LANGUAGE=Dutch google-drive-file-translator
```

Replace the placeholders with your actual values:

* `your_openai_api_key`: Your OpenAI API key.
* `your_input_folder_id`: ID of the input folder in Google Drive.
* `your_output_folder_id`: ID of the output folder in Google Drive.
* `credentials.json`: Path to your Google Drive API credentials file.
* `desired_language`: The full name of the language you want the files to be translated to.

## Acknowledgments

This project uses the following third-party libraries:

* OpenAI API
* Google Drive API
* Python 3.7+
* Docker
