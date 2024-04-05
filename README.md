# MUICT CHATBOT

Chatbot application for MUICT, a project for ITCS498 Special Topic in Computer Science semester 2 of 2023 at faculty of ICT, Mahidol University

## Members

| Name | ID | GITHUB |
|------|----|--------|
| Kittipich Aiumbhornsin | 6488004 | <https://github.com/ngzh-luke> |
| Linfeng Zhang | 6488168 | [https://github.com/Lr1zz]|
| [Name] | [ID] | [GitHub]|

## Prerequisites

- Python 3
- A Web Browser
- Cloned or downloaded the project

## Instructions

1. change working directory on terminal using `cd` command to where the project is saved

2. create virtual environment by run command:
`python -m venv venv`

3. activate virtual environment (macOS) by run command:
`source venv/bin/activate`
activate virtual environment (Windows) by run command: `venv\Scripts\activate`

4. check to see which environment is active by run command: `which pip`

5. install project dependencies by run command:
`pip install -r requirements.txt`

6. run command to start the application (browser will not open automatically):
`streamlit run src/main.py --server.headless true`
if you want to open the browser automatically please instead run: `streamlit run src/main.py`

7. check out the running application on browser by navigate to: `127.0.0.1:8501`
