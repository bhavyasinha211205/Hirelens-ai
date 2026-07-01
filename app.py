from flask import Flask, request, jsonify
from similarity import semantic_match

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "HireLens AI Service Running"
    })


@app.route("/similarity", methods=["POST"])
def similarity():

    try:

        data = request.get_json()

        parsed_jd = data.get("parsedJD", {})
        parsed_resume = data.get("parsedResume", {})

        jd_skills = parsed_jd.get("skills", [])

        result = semantic_match(
            jd_skills,
            parsed_resume
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )