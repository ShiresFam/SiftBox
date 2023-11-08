# SiftBox

## Description

SiftBox is an application that allows users to manage their emails. It provides features such as replying to emails, managing email threads, and more.

## Demo

[Here](https://youtu.be/iq9dsWxIXAQ) is a demo video that we created for our project.

## Installation

To install and run SiftBox, you'll need Docker and Docker Compose installed on your machine. Then, follow these steps:

1. Clone this repository: `git clone https://github.com/ShiresFam/SiftBox`
2. Navigate to the project directory: `cd SiftBox`
3. Create a `.env` file in the `./server` directory with the following variables:
    - `OPENAI_API_KEY`: Your OpenAI API key
    - `CLIENT_ID`: Your client ID
    - `CLIENT_SECRET`: Your client secret
  - I can provide these if needed for Hackathon testing. CLIENT_ID and CLIENT_SECRET are for Microsoft Azure App which gives us access to o365 APIs.
4. Start the application: `docker-compose up --build`

## Usage

Once the application is running, you can access it at `https://localhost:8443`. 

## Features

- Reply to emails
- Manage email threads
- Create TODO List
