# Seed Chat GPT with Contextual Sales Data

This repo explores the idea that we can seed Chat GPT with contextual CSV sales order data. So that 
a user can ask natural language questions and get back details about certain order data (related to a single customer).  

These could be things like order status, when an order was shipped, expected delivery date, what items are on the order, the total quantity on the order, and more.
The sales order data could be provided from any data source, so any ecommerce company could 
leverage this kind of technology. It could be used by internal stakeholders or by external customers engaging in an AI chat bot.

## How It Works

A sample CSV sales data is provided in the data folder, and loaded into a Pandas dataframe by the app.

A POST request to the endpoint passes a customer ID and a question/request about the data.  The customer ID is used to parse the dataframe 
to get only order data that pertains the customer by their ID.  

The Chat GPT 4 API is then called, providing the CSV data as "system content".  Then a "user content" question is asked about the
data in a natural language format.  Some examples that I successfully tested for customer 778:

* What is the status of the order that I placed on 5/7/04?
* What is the status of order 10248?
* List all the product codes on order 10329
* What is the total quantity ordered for order number 10107?
* List the distinct product lines on order 10292
* How many different orders do I have?
* What are the dates that I placed my orders?

## Installation

Requires Python 3.8 or newer.

Create an [openai account](https://platform.openai.com/) if you do not already have one.

Obtain an API key from the [api keys](https://platform.openai.com/account/api-keys) account page, and seed your account with money to make requests. 
As of 9/29/2023 you could seed your account with as little as $10 to get started.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages from requirements.txt.

```bash
pip install -r requirements.txt
```

Set your api key in your .zshrc file.

```bash
export CHATGPT_API_KEY=your-api-key-from-your-openai-account
```

## Usage

Start the development server:

```bash
python app.py
```

Example curl POST request:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"customer_id":"778","user_request":"List the distinct product lines on order 10292"}' \
  http://localhost:5000/api/chat
```

Example response:

```json
{
  "response": "The distinct product lines on order 10292 are:\n\n1. Classic Cars\n2. Trucks and Buses\n3. Trains"
}
```

## Visuals

![distinct product lines response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/distinct-product-lines-response.png?raw=true)
![distinct product lines csv](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/distinct-product-lines-csv.png?raw=true)

![total quantity ordered response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/total-quantity-ordered-response.png?raw=true)
![total quantity ordered csv](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/total-quantity-ordered-csv.png?raw=true)

![order status by date response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/order-status-by-date-response.png?raw=true)
![order status by date csv](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/order-status-by-date-csv.png?raw=true)

## Failure At Basic Math

Even though the technology will continue to get better and better, I've learned that the 9/29/2023 version of Chat GPT 4 does sometimes has trouble with basic math. 
For example, I asked the question:

What is the average price each for items on order 10292?

The correct answer is $79.43.

Here is the output from Chat GPT 4: 

```
To find the average price each for items on order 10292, we need to add up all the prices for this order and divide by the number of items. \n\nHere are the prices for each item on order 10292: \n\n100.0, 100.0, 30.06, 100.0, 55.07, 67.73, 100.0, 53.75, 100.0, 100.0, 100.0, 46.53\n\nAdding these up gives us a total of 1053.11. \n\nThere are 12 items on this order, so we divide 1053.11 by 12 to get the average price each. \n\n1053.11 / 12 = 87.76\n\nSo, the average price each for items on order 10292 is approximately 87.76.
```

The interesting thing to note here is that it did identify all the prices correctly.  But, if you take out your calculator and add up all those prices it is not 1053.11, 
but rather 953.14. The number of line items of 12 is correct.  And if the sum was actually 1053.11 then the answer of 87.76 would also be correct.  However, the correct 
math is 953.14 / 12 = 79.43.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)