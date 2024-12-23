from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from fsa import TimeExpressionFSA
import re

app = Flask(__name__)
fsa = TimeExpressionFSA()

@app.route("/process", methods=["POST"])
def process_time_expression():
    data = request.json
    text = data.get("text", "")
    matches = fsa.process_input(text)
    final_date = fsa.calculate_combined_datetime(matches)
    if final_date:
        result = final_date.strftime("%A, %d %B %Y %I:%M %p")
    else:
        result = "No valid date found"
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)