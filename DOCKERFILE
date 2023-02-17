FROM python:3.9.16-bullseye

ENV PROJECT_DIR /app

WORKDIR /app
RUN pip install pipenv

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

WORKDIR ${PROJECT_DIR}
COPY Pipfile .
# COPY Pipfile.lock .

RUN pipenv install
# RUN pipenv install --system
# RUN pipenv install --system --deploy
COPY . .

# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]