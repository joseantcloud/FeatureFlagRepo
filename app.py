from flask import Flask, render_template
from featuremanagement import FeatureManager
from azure.appconfiguration.provider import load, WatchKey


### connection string from our Application
APP_CONFIG_CONNECTION_STRING = ""

app = Flask(__name__)

# configs to load
config = load(
    connection_string=APP_CONFIG_CONNECTION_STRING,
    refresh_interval=10,
    feature_flag_enabled=True,
    feature_flag_refresh_enabled=True
)

feature_manager = FeatureManager(config)


## routes from flask
@app.route("/")
def index():
    try:
        config.refresh()
    except Exception:
        pass

    survey_on = feature_manager.is_enabled("SurveyON")
    print(survey_on)
    return render_template("index.html", survey_on=survey_on)

if __name__ == "__main__":
    app.run(debug=True, port=5000)