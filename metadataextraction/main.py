from flask import Flask
import langchain_metadata

app = Flask(__name__)

@app.route("/metadata")

def metadata(): 
    return langchain_metadata.main()

if __name__ == "__main__":
    app.run(debug=True)
