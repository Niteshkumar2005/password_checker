from flask import Flask, render_template, request
import string

app = Flask(__name__)

def check_password_strength(password):
    lower_count = sum(1 for c in password if c.islower())
    upper_count = sum(1 for c in password if c.isupper())
    num_count = sum(1 for c in password if c.isdigit())
    wspace_count = password.count(' ')
    special_count = sum(1 for c in password if c in string.punctuation)

    strength = 0
    if len(password) >= 8: strength += 1
    if lower_count: strength += 1
    if upper_count: strength += 1
    if num_count: strength += 1
    if special_count: strength += 1

    percentage = (strength / 5) * 100
    suggestions = []
    if len(password) < 8: suggestions.append("Increase length to at least 8 characters.")
    if not lower_count: suggestions.append("Add lowercase letters.")
    if not upper_count: suggestions.append("Add uppercase letters.")
    if not num_count: suggestions.append("Add numbers.")
    if not special_count: suggestions.append("Add special characters.")

    return {
        "lower": lower_count,
        "upper": upper_count,
        "numbers": num_count,
        "whitespace": wspace_count,
        "special": special_count,
        "length": len(password),
        "percentage": percentage,
        "suggestions": suggestions
    }

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        password = request.form.get("password")
        result = check_password_strength(password)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
