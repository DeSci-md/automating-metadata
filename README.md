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
Requires the habanero python package for searching crossref (https://pypi.org/project/habanero/)

```shell
pip install habanero
```

For calling the Elsevier API, the httpx module is used.

```shell
pip install httpx
```

For XML file parsing, the package BeautifulSoup is used, with lxml as an xml parser.

```shell
pip install beautifulsoup4
pip install lxml
```

# Web Interface/Client
Current progress is being tracked by [signal-k/client](http://github.com/Signal-K/client/pull/19) and will be added as a git submodule once our generator & metadata smart contracts are completed

## Generative API
### Containerisation for local development

In root dir, `Dockerfile` runs the Flask Server in a container.

The `docker-compose.yml` defines a cluster with the Server and a local PostgreSQL container

For convenience, a Makefile supports the following simple operations:

* `make build` builds an image from the current working copy
* `make run` starts the cluster, rebuilding if necessary
* `make logs` tails the logs for both containers
* `make stop` stops and deletes the clusters

For rapid iteration, I use:
`make stop run logs`

#### Prerequisites

You will need to have a Docker environment available... Docker Desktop or an equivalent

#### Previous Issues

##### ThirdWeb

The build step (`make build`) fails whilst running `pipenv install` during the build of the Docker image.

`thirdweb-sdk` caused errors on `pipenv install`. The output was long and ugly; but a resolution has been found.
The problem was the use of the `slim-` base image.  Switching from `p`ython:3.9.9-slim-bullseye` to `python:3.9.9-bullseye` avoided the problem.

##### Ventura - Flask default port 5000

Flask runs by default on port 5000.  However, on macos Ventura, there is a system service "Airplay Receiver" listening on this port.

In this case, `localhost:5000` does not reach the Flask app, although `127.0.0.1:5000` does.

The easiest solution is to turn off the Airplay Receiver service; an alternative is to run Flask on a different port... perhaps 7355 for TESS?

#### Current Issue

The server responds to `http://localhost:5000` with a classic "Hello World"

Several of the blueprints in `app.py` are commented out since they have dependencies on ThirdWeb

# Flask blueprints
For now, each flask file is located in the root directory of this repository - however they'll be moved into their own folders with their respective models, views and controllers down the line