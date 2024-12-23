from flask import Flask, request, jsonify
from datetime import datetime
from fsa import TimeExpressionFSA

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_time_expression():
    data = request.json
    text = data.get("text", "")
    current_time = datetime.now()
    fsa = TimeExpressionFSA(today=current_time)
    matches = fsa.process_input(text)
    final_date = fsa.calculate_combined_datetime(matches)
    if final_date:
        result = final_date.strftime("%A, %d %B %Y %I:%M %p")
    else:
        result = "No valid date found"
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)