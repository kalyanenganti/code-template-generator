# code-template-generator
Generates code template for selected user language
Run the following to setup the backend project


#BACKEND API
1. git clone https://github.com/kalyanenganti/code-template-generator
2. python -m venv venv
3. venv/Scripts/activate.bat (for windows) or source venv/bin/activate (for linux)
4. pip install -r requirements.txt
5. fastapi dev main.py (for dev ) fastapi run (prod)



#TEST SUITE
Instructions for Running the Test Suite

Install dependencies: pip install pytest syrupy (syrupy handles snapshot assertions; it's lightweight and integrates seamlessly with pytest).
Ensure your backend module (e.g., main.py) is in the project root, and tests/ directory exists with the test_generators.py.
Run the tests: pytest tests/test_generators.py

On first run, syrupy will generate snapshot files in a __snapshots__/ directory within tests/. These store the expected template strings.
If templates change (e.g., due to code updates), run pytest tests/test_generators.py --snapshot-update to regenerate snapshots, then commit them to version control.
For verbose output: pytest -v tests/test_generators.py

Validation:
Navigate to http://<your_hostname>:8000/docs to access the swagger UI.
Click on the post /api/vi/template request try it out:
Paste the following in the request body and press execute:
"{
"question_id": "two-sum",
"title": "Two Sum",
"description": "Given an integer array...",
"signature": {
"function_name": "twoSum",
"parameters": [
{ "name": "nums", "type": "int[]" },
{ "name": "target", "type": "int" }
],
"returns": { "type": "int[]" }
},
"language": "python"
}"
You should see the repsonse if the request is successful or error if any with the message.
<img width="1334" height="652" alt="image" src="https://github.com/user-attachments/assets/e2d5c8f8-cc04-4c18-b603-661acefbb35b" />
