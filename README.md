# automating-metadata

A central place to drop all of our experiments! As a disclaimer - we're still at the experimentation phase! Lots of this code will change. 

The core of this project is to see how we can use LLM and other technology available to us to respond to the following problems (not an exhaustive list): 

1. Metadata is non-standard/incomparable. 
2. Metadata is inconsistently applied.
3. Metadata is inflexible

These features create a problem that makes relevant literature difficult to connect to each other, leaves the decision of what metadata to include up to researchers or journals, and requires a standard application to be useful. We then end up with inconsistent metadata that can't connect research projects either to their own research objects like the code and data associated with them, or to other papers that might be relevant. These issues make academic search and representing an accurate 'map' of science extremely difficult. 

We hope to see how we can create a flexible metadata standard that accurately connects papers both to their own additional materials and to other research based on as much data as we can gather. 

We're operationalizing this problem as: 

How might we reliably automate a literature review? 

## Publication Text Extraction
### Aim/Goal
The aim/goal of this is to provide a way to programmatically extract machine-readable text from journal publications when provided an identifier such as a title or DOI.
Adapted using the methodology described in https://www.nature.com/articles/s41524-021-00687-2, "Automated pipeline for superalloy data by text mining"

### Setup and use

Make sure you have Docker installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).

### Clone the Repository

```bash
git clone https://github.com/DeSci-md/automating-metadata.git
cd your-repository
```

### Build the Docker Image

```bash
docker build -t automating-metadata-v1.
```

### Run the Docker Container

```bash
docker run -p 5001:5001 automating-metadata-v1
```

The application will be available at `http://localhost:5001/invoke-script`.

#### Endpoint

The application exposes a single endpoint:

**POST /invoke-script**
- **Request Body**: JSON object with `pdf` and `doi` fields
- **Response**: JSON object with `output` field containing the result of the `langchain_orcid2.run()` function

Example request:
```json
{
  "pdf": "path/to/pdf/file",
  "doi": "10.1234/example-doi"
}
```

Example response:
```json
{
  "output": "Result of the script execution"
}
```

### Endpoint
If you would like to contribute to this project, please follow these guidelines:
- Fork the repository
- Create a new branch for your feature or bug fix
- Make your changes and commit them
- Push your branch to your forked repository
- Submit a pull request to the main repository

### Credits

This project uses the many third-party libraries documented in the requirements file!

### License
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

