![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

![CI-CD-ml passing](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-fizzbuzz-2/actions/workflows/CI-CD-ml.yml/badge.svg)

![CI-CD-webapp passing](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-fizzbuzz-2/actions/workflows/CI-CD-webapp.yml/badge.svg)

# Monolingo

## Team members

- [Dhiyaa Al Jorf](https://github.com/DoodyShark)

- [Firas Darwish](https://github.com/FirasBDarwish)

- [Shubhi Upadhyay](https://github.com/shubhiupa19)

## Project Description

Monolingo is a language learning app that teaches you english pronounciation from... english. Not exactly the most useful but oh well haha. Monolingo presents users with a set of sentences they need to practice, and stores their scores (by associating with their current cookie rather than by creating permanent users). To check pronunciation, Monolingo sends the user input to Meta-AI's Speech2Text machine learning model and checks whether the output matches. Metadata and training sentences are stored on a mongoDB database.

## Configure and Run

Configuring and running the application is very easy. Add the .env files following the .env-example files. After cloning the repository, run the following command in the repo's root directory.

```console
$ docker compose up --build
```

This should start up all tools and populate mongoDB with any necessary data for the system to run.

## Image Sources

- favicon: [Emoticons created by Royyan Wijaya - Flaticon](https://www.flaticon.com/free-icons/emot)
