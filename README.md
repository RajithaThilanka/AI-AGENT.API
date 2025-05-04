# AI-AGENT.API

A Python-based API service that provides AI-powered travel assistance and recommendations.

## Project Structure

```
AI-AGENT.API/
├── Pipfile
├── Pipfile.lock
├── main.py
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── services/
│       ├── __init__.py
│       └── travel_chain.py
└── .env
```

## Prerequisites

- Python 3.8 or higher
- pipenv (Python package manager)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-AGENT.API
```

2. Install dependencies using pipenv:
```bash
# Option 1: Using install script (Recommended)
pipenv run install

# Option 2: Manual installation
pipenv install
```

3. Create a `.env` file in the project directory with your environment variables:
```env
# Add your environment variables here
```

## Running the Application

You can start the application in two ways:

### Option 1: Using pipenv run (Recommended)
```bash
pipenv run start
```

### Option 2: Manual start
1. Activate the virtual environment:
```bash
pipenv shell
```

2. Start the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000` by default.

## Development

- The API routes are defined in `app/api/routes.py`
- Core configuration is in `app/core/config.py`
- AI services are implemented in `app/services/travel_chain.py`

## License

[Add your license information here]
