# WeatherApp

A simple Flask app that lets a user enter a city and displays the current weather with an icon.

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Create a `.env` file in the project root or set your OpenWeatherMap API key in the environment.

- Copy `.env.example` to `.env` and update the value:

```text
OPENWEATHERMAP_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key
```

- Or set the environment variables directly in PowerShell:

```powershell
setx OPENWEATHERMAP_API_KEY "your_api_key_here"
setx FLASK_SECRET_KEY "your_secret_key"
```

3. Restart your terminal session after using `setx` so the new environment variables are available.

## Run

1. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

2. Start the app:

```powershell
python app.py
```

3. Open this URL in your browser:

```text
http://127.0.0.1:5000
```

### Alternative Windows shortcut

Run `start-weather.bat` from the project folder to activate the venv and start the server automatically.
