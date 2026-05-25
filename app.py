import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
import requests


def load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")

OWM_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_for_city(city_name: str, units: str = "metric"):
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENWEATHERMAP_API_KEY environment variable is not set."
        )

    params = {
        "q": city_name,
        "appid": api_key,
        "units": units,
    }
    print(f"[Weather API] Requesting: {city_name} | API key present: {bool(api_key)}")
    response = requests.get(OWM_URL, params=params, timeout=10)
    print(f"[Weather API] Status: {response.status_code}")
    response.raise_for_status()
    data = response.json()

    return {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature": data.get("main", {}).get("temp"),
        "description": data.get("weather", [{}])[0].get("description", ""),
        "icon": data.get("weather", [{}])[0].get("icon", ""),
        "humidity": data.get("main", {}).get("humidity"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "units": units,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    city = ""
    units = request.form.get("units", "metric")

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            flash("Please enter a city name.", "error")
            return redirect(url_for("index"))

        try:
            weather = get_weather_for_city(city, units=units)
        except requests.HTTPError as http_err:
            if http_err.response.status_code == 404:
                flash("City not found. Please try another city.", "error")
            elif http_err.response.status_code == 401:
                flash("API key is invalid. Check your OPENWEATHERMAP_API_KEY in .env.", "error")
            elif http_err.response.status_code == 429:
                flash("Too many requests. Please wait a moment and try again.", "error")
            else:
                try:
                    error_detail = http_err.response.json().get("message", "")
                    msg = f"Weather API error ({http_err.response.status_code}): {error_detail}"
                except:
                    msg = f"Weather service error ({http_err.response.status_code}). Please try again."
                flash(msg, "error")
        except RuntimeError as runtime_err:
            flash(str(runtime_err), "error")
        except requests.RequestException:
            flash("Unable to retrieve weather data. Check your network connection.", "error")
    elif not os.environ.get("OPENWEATHERMAP_API_KEY"):
        flash(
            "OPENWEATHERMAP_API_KEY is not set. Create a .env file or export the variable.",
            "error",
        )

    return render_template("index.html", weather=weather, city=city, units=units)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
