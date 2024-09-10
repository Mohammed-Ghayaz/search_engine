from flask import Flask, request, jsonify, render_template
import pandas as pd
from fuzzywuzzy import process

# Initialize the Flask app
app = Flask(__name__)

# Load the Excel dataset
df = pd.read_excel("Alumni List.xlsx")


# Define the search functionality
def find_name(partial_name):
    # Perform fuzzy matching to find the closest match
    matched_names = df[df['fullname'].str.contains(partial_name, case=False, na=False)]

    if matched_names.empty:
        return "No match found."
    else:
        return matched_names[['fullname', 'linkedin']]


# Route for the search form
@app.route('/')
def search_form():
    return "Search Engine"


# Route to handle search functionality
@app.route('/search', methods=['POST'])
def search():
    partial_name = request.form.get('name')
    results = find_name(partial_name)

    if isinstance(results, str):  # If no match found
        return jsonify({"message": results})
    else:
        # Return results as JSON
        return results.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
