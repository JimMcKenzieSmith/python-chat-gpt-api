import pandas as pd
import openai
import os
from flask import Flask, request, jsonify

openai_model = 'gpt-4'

app = Flask(__name__)


@app.route('/api/sales', methods=['POST'])
def get_sales():
    try:
        openai.api_key = os.getenv('CHATGPT_API_KEY')

        # load up all the sample CSV customer sales data into a data frame 
        # (obviously, we would not normally first load up ALL the sales data, but rather SQL query based on the customer ID)
        df = pd.read_csv('data/sales_data_sample.csv')

        # Get the POST request's JSON data
        data = request.get_json()

        # Get the customer ID from the post json
        customer_id = int(data['customer_id'])

        # Get the customer's question from the post json
        user_request = data['user_request']

        # search for rows with a customer ID (value that is passed in via an API)
        # get one customer's data into a dataframe to give chatgpt context to the chat conversation
        df = df[df['CUSTOMER_ID'] == customer_id]

        # chat gpt gives more accurate repsonses if the csv data is sorted by the order number, so that line items are grouped together
        df = df.sort_values('ORDER_NUMBER')

        # TODO: work the customer's fist name into the chat response
        # customer_first_name = customer_data['CONTACT_FIRST_NAME'].iloc[0]

        system_prompt = 'Use this CSV order data when answering questions'

        # Get a response from Chat GPT-4
        response = get_response_from_chat_gpt(df.to_csv(index=False), system_prompt, user_request, 0)

        return response, 200
    except KeyError:
        return jsonify({'error': 'customer_id and user_request are required inputs in the POST request JSON data'}), 400

@app.route('/api/quiz-results', methods=['POST'])
def get_quiz_results():
    try:
        openai.api_key = os.getenv('CHATGPT_API_KEY')

        # Get the POST request's JSON data
        data = request.get_json()

        file_loc = data['file_loc']
        user_request = data['user_request']

        # load up the classroom quiz data into a dataframe
        df = pd.read_csv(file_loc)

        # sort the data by question ID to see if we get a better response from chat gpt
        df = df.sort_values('QUIZ_QUESTION_ID')

        system_prompt = 'Use this CSV quiz result data, from a 5th grade classroom, when answering questions'

        # Get a response from Chat GPT-4
        response = get_response_from_chat_gpt(df.to_csv(index=False), system_prompt, user_request, 0.2)

        return response, 200

    except KeyError:
        return jsonify({'error': 'file_loc and user_request are required inputs in the POST request JSON data'}), 400

def get_response_from_chat_gpt(csv_data, system_prompt, user_request, chat_temerature):
        openai_response = openai.ChatCompletion.create(
            model = openai_model,
            messages = [
                {"role": "system", "content": system_prompt + ": \n" + csv_data},
                {"role": "user", "content": user_request}
            ],
            # The sampling temperature can be a range between 0 and 2. Higher values like 0.8 will make the output more random, 
            # while lower values like 0.2 will make it more focused and deterministic. Our use case is very deterministic, so we use a low number.
            temperature = chat_temerature
        )

        return {'response': openai_response.choices[0].message.content}

if __name__ == '__main__':
    app.run(debug=True)
