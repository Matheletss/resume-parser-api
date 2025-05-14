# Resume Parser API

## Overview
This is a Python-based API for parsing and extracting information from resumes.

## Prerequisites
- Python 3.10+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Matheletss/resume-parser-api.git
cd resume-parser-api
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
sudo apt update
sudo apt install -y tesseract-ocr poppler-utils(For Windows download the .exe and add to local path)
python -m spacy download en_core_web_sm
```

## Running the API

1. Ensure you're in the project directory and virtual environment:
```bash
source venv/bin/activate  # Activate virtual environment
```

2. Start the API:
```bash
# In resume-parser-api directory
uvicorn main:app --host 0.0.0.0 --port 8000
```
# In hirena-web directory
```
npm install
npm run dev
```
## Usage

- The API will typically run on `http://localhost:8000`
- Use endpoints to parse resumes and extract information

## Dependencies
- See `requirements.txt` for a full list of Python package dependencies

## Troubleshooting
- Ensure all dependencies are installed
- Check that you're using a compatible Python version
- Verify the input PDF/text file format

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
