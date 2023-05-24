# Python Question and Answer Chatbot

This is a Python Question and Answer Chatbot that uses OpenAI's GPT-3.5 language model to provide answers to frequently asked questions (FAQs).

## Description

The Question and Answer Chatbot allows users to ask questions and receive answers based on a predefined set of FAQs. It uses the GPT-3.5 language model to generate responses based on the user's questions and the closest matching FAQ.

The chatbot follows the following workflow:

1. User enters a question in the input form.
2. The chatbot finds the best matching FAQ based on the user's question.
3. The chatbot uses the matched FAQ and the user's question to generate a response using the GPT-3.5 model.
4. The generated answer is displayed to the user.

The chatbot also incorporates keyword matching and similarity scoring to improve the matching process and provide accurate answers.

## Features

- Simple and intuitive user interface.
- Matching of user's question with closest FAQ using similarity scoring.
- Integration with OpenAI's GPT-3.5 model for generating responses.
- Keyword matching to improve matching accuracy.
- HTML templating using Jinja2 for rendering the chatbot interface.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/yura-hudzovskyi/python-assistant.git
```
2. Navigate to the project directory:

```shell
cd python-assistant
```

3. Install the required packages:

```shell
pip install -r requirements.txt
```

4.  Set up the OpenAI API key:
   - Obtain an API key from OpenAI.
   - Set the OPENAI_API_KEY environment variable with your API key.

5. Run the application:
    
```shell
uvicorn main:app --reload
```

6. Access the chatbot in your browser:

- Open http://localhost:8000 in your web browser.
- Enter a question in the input form and submit.
- The chatbot will display the answer based on the best matching FAQ.