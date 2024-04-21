# MUICT CHATBOT

Chatbot application for MUICT, a project for ITCS498 Special Topic in Computer Science semester 2 of 2023 at faculty of ICT, Mahidol University

## Members

| NAME | ID | GITHUB |
|------|----|--------|
| Kittipich Aiumbhornsin | 6488004 | <https://github.com/ngzh-luke> |
| Tawan Chaidee | 6488011 | <https://github.com/tawan-chaidee> |
| Linfeng Zhang | 6488168 | <https://github.com/Lr1zz>|

## Prerequisites

- Python 3
- Docker
- A Web Browser
- Cloned or downloaded the project

## Instructions

1. change working directory on terminal using `cd` command to where the project is saved

2. create virtual environment by run command:
`python -m venv venv`

3. activate virtual environment (macOS) by run command:
`source venv/bin/activate`
activate virtual environment (Windows) by run command: `venv\Scripts\activate`

4. check to see which environment is active by run command: `pip --version`

5. install project dependencies by run command:
`pip install -r requirements.txt`

6. start up api server with command: `uvicorn src.apis.main:app`

7. open another terminal and run command to start the application (browser will not open automatically):
`streamlit run src/ui/main.py --server.headless true`
if you want to open the browser automatically please instead run: `streamlit run src/ui/main.py`

8. check out the running application on browser by navigate to the given URL from the terminal.
