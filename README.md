# PonderPoll
## Where thoughts become votes

PonderPoll is an app that lets you create and share polls with the world.
You can ask any question you want, and see how other people vote.
You can also browse and vote on polls created by other users, and discover
what they think about various topics.

## Installation

### Pre-requisites

To install PonderPoll make sure that you already have Docker and Docker Compose
installed on your local machine.
Check out docker documentation to install:
- Docker: https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

### Clone the repository to your local machine

`git clone https://github.com/AndrewYatskevich/ponder-poll.git`

### Move to the root folder of the project

`cd ponder-poll/`

### Create the .env file and fill it out

- Create the .env file `touch .env`
- Fill out the .env file by referring to .env.example

### Run Docker Compose to spin up the application

`docker compose -f docker-compose.yaml up -d`

## Usage

The application is available on 0.0.0.0:8000 host.
The following functionality has been implemented:
- User registration and authentication
- CRUD operations with polls and their options
- Ability to vote for the desired option in a poll

To learn about all possibilities, check out the documentation please:
- Move to docs folder `cd ponder_poll/docs/_build/html/`
- Open the index.html in your browser

## Features

The following features have been implemented:
- Integration with third-party API to get different facts about the world
- Asynchronous data processing and cache usage to improve user experience
- Background daily task to save poll statistical information to a .csv file

## License
MIT © [Andrew Yatskevich](https://github.com/AndrewYatskevich)
