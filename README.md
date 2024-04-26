# MUICT CHATBOT

Chatbot application for MUICT, a project for ITCS498 Special Topic in Computer Science semester 2 of 2023 at faculty of ICT, Mahidol University. The models are trained to know about MUICT, mostly on information on 2 year courses, therefore, with a limited rage of data trained, it might not enough to generates such a relevent responses, or even generates bias responses and incorrect information.

## On this file

- [MUICT CHATBOT](#muict-chatbot)
- [Members of group 4](#members-of-group-4)
- [Prerequisites](#prerequisites)
- [First things first](#first-things-first)
- [Instructions (Python interpreter)](#instructions-python-interpreter)
- [Instructions (Docker)](#instructions-docker)
- [Deployment (Backend)](#deployment-backend)
- [Deployment (Frontend)](#deployment-frontend)

## Members of group 4

| NAME | ID | GITHUB |
|------|----|--------|
| Kittipich Aiumbhornsin | 6488004 | <https://github.com/ngzh-luke> |
| Tawan Chaidee | 6488011 | <https://github.com/tawan-chaidee> |
| Linfeng Zhang | 6488168 | <https://github.com/Lr1zz>|

## Prerequisites

- A machine with a specification to handle high workload with a high performance GPU
- Python 3
- Docker (if would like to run chat UI(frontend) using Docker)
- A Web Browser
- Cloned or downloaded the project

## First things first

- For the backend, due to the model is large and requires a huge amount of machine resorces, therefore the machine specification that we tested and works fine (with low traffic) are listed below:
  - **CPU**: Intel(R) Xeon(R) CPU @ 2.00GHz: 2 vCPU (1 core) with 13GB of RAM
  - **GPU**: 1 Nvidia T4

- For the frontend, you may choose to run using Docker or directly using Python interpreter (Instructions in section below)

## Instructions (Python interpreter)

1. change working directory on terminal using `cd` command to where the project is saved.

2. create virtual environment by run command:
`python -m venv venv`

3. activate virtual environment (macOS) by run command:
`source venv/bin/activate`
activate virtual environment (Windows) by run command: `venv\Scripts\activate`

4. check to see which environment is active by run command: `pip --version`

5. install project dependencies by run command:
`pip install -r requirements.txt`

6. create the `.env` or `.dev.env` file and specify all of the key-value pairs, please refer to file `.example.env` for key-value pairs details.

7. start up api server with command: `uvicorn src.apis.main:app`

8. open another terminal and run command to start the application (browser will not open automatically):
`streamlit run src/ui/main.py --server.headless true`
if you want to open the browser automatically please instead run: `streamlit run src/ui/main.py`

9. check out the running application on browser by navigate to the given URL from the terminal.

## Instructions (Docker)

1. change working directory on terminal using `cd` command to where the project is saved.

2. build Docker image by using command: `docker build -f Dockerfile.ui -t chatui .`

3. after build is success, run the frontend server by using command: `docker run --name chatui -it -p 8501:8501`

4. navigate to browser and visit chat UI via `127.0.0.1:8501` or `0.0.0.0:8501`

## Deployment (Backend)

In this instructions, we will deploy our backend to a cloud linux instance by using NGINX as a web server.

### Things to know before proceed

    1. This instruction is adapted from 2 blog posts which you can find them [here](resources.md)
    2. A linux instance with GPU
    3. There are quite a lot of command lines operations, you may need to be familar with terminal stuff
    4. 

1. connect to the cloud instance by ssh to it by using command: `ssh [your instance username]@[your instance IP]
2. 

## Deployment (Frontend)

We will deploy our frontend to a cloud linux instance by using a Docker container.

### Prerequisites for follow this instructions

    1. Container Registry (In this case is Google Artifact Registry)
    2. Google Cloud CLI
        2.1 Already logged in and setup the Google Cloud project
    3. Frontend Docker image
    4. You may replace some of the commands that fit your situations

0. you may update Docker config to enable to push to Artifact Registry by command: `gcloud auth configure-docker [Google cloud Region ID such as 'us-central1']-docker.pkg.dev` please note that you may find this command in the Artifact console as well

1. tag our Docker image that to be pushed to the registry by using command: `docker tag [the image you built]:[your image tag] [Google cloud Region ID such as 'us-central1']-docker.pkg.dev/[your Google Cloud project]/[Artifact repository]/[image name to show in Artifact]:[image tag]`

2. push Docker image to the Artifact Registry by using command: `docker push [Google cloud Region ID such as 'us-central1']-docker.pkg.dev/[your Google Cloud project]/[Artifact repository]/[image name to show in Artifact]:[image tag]`

3. 
