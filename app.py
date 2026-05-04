import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '').lower()
    
    # चेक करने के लिए कुछ स्किल्स
    keywords = ["python", "java", "sql", "html", "css", "javascript", "react", "excel"]
    found = [word for word in keywords if word in text]
    
    score = (len(found) / len(keywords)) * 100 if keywords else 0

    return jsonify({
        "score": round(score, 2),
        "skills_found": found
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)
 @app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return "File uploaded successfully ✅"   
