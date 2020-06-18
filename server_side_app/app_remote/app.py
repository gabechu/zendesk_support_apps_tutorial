import os

import requests
from flask import Flask, make_response, render_template, request

app = Flask(
    __name__, static_url_path="", static_folder="static", template_folder="templates"
)


@app.route("/sidebar")
def send_iframe_html():
    qs = request.query_string.decode("utf-8")
    response = make_response(render_template("start.html", qs=qs))
    response.set_cookie("my_app_params", qs)
    return response


@app.route("/list")
def show_tasks():
    project_id = "1179744536702849"
    access_token = os.environ.get("ASANA_API_TOKEN")
    header = {"Authorization": f"Bearer {access_token}"}
    url = f"https://app.asana.com/api/1.0/projects/{project_id}/tasks"
    r = requests.get(url, headers=header)

    if r.status_code == 200:
        tasks = r.json()
        return render_template(
            "list_tasks.html", tasks=tasks["data"], project_id=project_id
        )
    else:
        msg = f"Problem with the request: {r.status_code} {r.reason}"
        qs = request.cookies.get("my_app_params")
        return render_template("start.html", qs=qs, error_msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
