# Livinit-back

## Instructions

First, ask the team for credentials to add to your .env file.

```
# Create .env file from template
cp .env.example .env
```

Create a Virtual Environment in Python:
```
python -m venv .venv
source .venv/bin/activate
```

Install requirements:
```
python -m pip install -r requirements.txt
```

Run the backend:
```
uvicorn main:app --reload
```

See the UI in http://127.0.0.1:8000/docs

Example:

POST /recommend
```
{
  "style": "minimalist",
  "budget": 3500,
  "prompt": "Incorporate a sectional sofa and a large coffee table in the bohemian-style living room for six people, Under $3500."
}
```