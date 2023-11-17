# automating-metadata

A central place to drop all of our experiments! As a disclaimer - we're still at the experimentation phase! Lots of this code will change. 

The core of this project is to see how we can use LLM and other technology available to us to respond to the following problems (not an exhaustive list): 

1. Metadata is non-standard/incomparable. 
2. Metadata is inconsistently applied.
3. Metadata is inflexible

These features create a problem which makes relevant literature difficult to connect to each other, leaves the decision of what metadata to include up to researchers or journals, and requires standard application to be useful. We then end up with inconsistent metadata that can't connect research projects either to their own research objects like the code and data associated with them, or to other papers that might be relevant. These issues make academic search and representing an accurate 'map' of science extremely difficult. 

We hope to see how we can create a flexible metadata standard that accurately connects papers both to their own additional materials and to other research based on as much data as we can gather. 

We're operationalizing this problem as: 

How might we reliably automate a literature review? 

## Publication Text Extraction
### Aim/Goal
The aim/goal of this is to provide a way to programmically extract machine readable text from journal publication when provided an identifier such as a title or DOI.
Adapted using the methodology described in https://www.nature.com/articles/s41524-021-00687-2, "Automated pipeline for superalloy data by text mining"

### Setup and use

Make sure you have Docker installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).

### Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Build the Docker Image

```bash
docker build -t your-image-name .
```

### Run the Docker Container

```bash
docker run -e NODE_ENV=your-node-env -e DOI_ENV=your-doi-env your-image-name
```

Replace `your-node-env` and `your-doi-env` with the desired values for `NODE_ENV` and `DOI_ENV`.

### Setting Environment Variables

- **NODE_ENV**: This determines the node you want to get metadata for. EG: 46
- **DOI_ENV**: This is a DOI that corresponds to the node. if you do not have a DOI for the article, do not set this variable. 

You can set these environment variables using the `-e` option with the `docker run` command.

### Example

```bash
docker run -e NODE_ENV="46" -e DOI_ENV="10.3847/0004-637X/828/1/46" your-image-name
```

