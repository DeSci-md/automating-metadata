# Automating Author Identification

This is the first operational version of the automated metadata application. We've updated it to meet the requirements of the [DeSci Nodes](nodes.desci.com) application as a first use case. 

The core of this version of the project is to implement one quality-of-life improvement for submitting articles to pre-print servers. It is intended to address the tedium of manually inputting all the OrcIDs for each co-author on a paper and promote consistent application of the OrcID standard.

For documentation on the full scope of the Automating Metadata project see the documentation at the [Automating Metadata Repository](https://github.com/DeSci-md/automating-metadata). 

## Publication Text Extraction
### Aim/Goal
The aim/goal of this is to provide a way to return the author names, affiliations, and OrcID from publications when provided an identifier such as a DOI or any PDF (published or unpublished). See [endpoint](#endpoint) for an example of the input and outputs for the project. 

### Setup and use

Make sure you have Docker installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).

### Clone the Repository

```bash
git clone https://github.com/DeSci-md/automating-metadata-v1.git
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
  {"output":{"authors":{"M. Anonymous":{"@id":"https://orcid.org/0000-0000-0000-0000","affiliation":"Well-known Foundation","name":"Mark Anonymous","role":"Person"}},"title":"The title of the paper is \"The Extracted Title""}}
}
```

### Contribution
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

