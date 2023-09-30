import pandas as pd
import openai
import os
from flask import Flask, request, jsonify


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
        customer_data = df[df['CUSTOMER_ID'] == customer_id]

        # chat gpt gives more accurate repsonses if the csv data is sorted by the order number, so that line items are grouped together
        customer_data.sort_values(by=['ORDER_NUMBER'], inplace=True)

        # TODO: work the customer's fist name into the chat response
        # customer_first_name = customer_data['CONTACT_FIRST_NAME'].iloc[0]

        openai_response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": "Use this CSV order data when answering questions: \n" + customer_data.to_csv(index=False)},
                {"role": "user", "content": user_request}
            ],
            # The sampling temperature can be a range between 0 and 2. Higher values like 0.8 will make the output more random, 
            # while lower values like 0.2 will make it more focused and deterministic. Our use case is very deterministic, so we use a 0.
            temperature = 0 
        )

        # Create a JSON response
        response = {'response': openai_response.choices[0].message.content}

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
        df.sort_values(by=['QUIZ_QUESTION_ID'], inplace=True)

        openai_response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": "Use this CSV quiz result data, from a 5th grade classroom, when answering questions: \n" + df.to_csv(index=False)},
                {"role": "user", "content": user_request}
            ],
            temperature = 0.2
        )

        response = {'response': openai_response.choices[0].message.content}

        return response, 200

    except KeyError:
        return jsonify({'error': 'file_loc and user_request are required inputs in the POST request JSON data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
