# Train Chat GPT-4 With Your CSV Data

This repo explores the idea that we can train Chat GPT-4 with contextual CSV data. So that 
a user can ask natural language questions and get back insights, details, or action items to take around the data. 

For sales order data, this could be things like order status, when an order was shipped, expected delivery date, what items are on the order, the total quantity on the order, or even analyzing the data and looking for patterns or trends.
The sales order data could be provided from any data source, so any ecommerce company could 
leverage this kind of technology. It could be used by internal stakeholders or by external customers engaging in an AI chat bot.

For classroom quiz or test data, the value-add could be creating a custom lesson plan based on which questions the most students had trouble answering correctly.

## How It Works

Sample CSV data files are provided in the data folder, and these get loaded into a Pandas dataframe by the app.

For the sales data endpoint, a POST request to the endpoint passes a customer ID and a question/request about the data.  The customer ID is used to parse the dataframe 
to get only order data that pertains the customer by their ID.  

The Chat GPT 4 API is then called, providing the CSV data as "system content".  Then a "user content" question is asked about the
data in a natural language format.  Some examples that I successfully tested for customer 778:

* What is the status of the order that I placed on 5/7/04?
* List all the product codes on order 10329
* What is the total quantity ordered for order number 10107?
* List the distinct product lines on order 10292
* How many different orders do I have?
* What are the dates that I placed my orders?
* Analyze the data and look for patterns or trends

For the quiz data endpoint, more information is provided below.

## Installation

Requires Python 3.8 or newer.

Create an [openai account](https://platform.openai.com/) if you do not already have one.

Obtain an API key from the [api keys](https://platform.openai.com/account/api-keys) account page, and seed your account with money to make requests. 
As of 9/29/2023 you could seed your account with as little as $10 to get started.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages from requirements.txt.

```bash
pip install -r requirements.txt
```

Set your api key in your .zshrc file if using a Mac.

```bash
export CHATGPT_API_KEY=your-api-key-from-your-openai-account
```

## Usage

Start the development server:

```bash
python app.py
```

Example curl POST request for sales data:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"customer_id":"778","user_request":"List the distinct product lines on order 10292"}' \
  http://localhost:5000/api/sales
```

Example response for sales data:

```json
{
  "response": "The distinct product lines on order 10292 are:\n\n1. Classic Cars\n2. Trucks and Buses\n3. Trains"
}
```

Example curl POST request for quiz data:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"file_loc":"data/cold_war_classroom_quiz_sample.csv","user_request":"What questions were answered 100% correct by all the students?"}' \
  http://localhost:5000/api/quiz-results
```

Example response for quiz data:

```json
{
  "response": "The questions that were answered 100% correct by all the students are:\n\n1. What was the significance of the Cuban Missile Crisis during the Cold War?\n2. What was the purpose of the Berlin Wall?"
}
```

## Visuals - Sales Data Responses

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

## Analyze The Data For Patterns or Trends

For customer ID 778, I asked the API to `Analyze the data and look for patterns or trends`.  Here is what it came back with:

```
As an AI model, I can provide a general analysis based on the given CSV data. Here are some observations:

1. Customer: All the orders are made by the same customer, \"Land of Toys Inc.\" located in NYC, NY, USA.

2. Order Status: There are two types of order statuses - 'Shipped' and 'Cancelled'. It might be interesting to investigate the reasons for cancellations.

3. Product Line: The orders are spread across different product lines including 'Motorcycles', 'Ships', 'Vintage Cars', 'Trains', 'Classic Cars', and 'Trucks and Buses'. 

4. Quantity Ordered: The quantity ordered varies significantly from order to order, ranging from 20 to 50 units.

5. Price: The price of each unit also varies, with some as low as 30.06 and others as high as 100. 

6. Order Dates: The orders are spread across different years (2003, 2004) and months, which could be used to analyze seasonal trends.

7. Deal Size: The deal sizes are categorized as 'Small', 'Medium', and 'Large'. It could be interesting to see the correlation between deal size, quantity ordered, and total sales.

8. Sales: The sales amount varies from order to order, which could be due to the differences in quantity ordered and unit price.

Please note that a more detailed analysis could be performed with specialized data analysis tools or software.
```

## Classroom Quiz Data on the Cold War

To expand this repo to include another CSV data use case, I've added a fictional 5th grade classroom quiz on the topic of the Cold War.  

See `data/cold_war_classroom_quiz_sample.csv` which has student ID's, quiz question ID's, quiz questions, and whether the student got the answer correct or incorrect. The data is denormalized. 
The idea here is that we are seeing if ChatGPT-4 can determine any meaning from this data and/or actionable next steps. 

My first idea was to produce a custom lesson plan based upon what questions were answered incorrectly by most of the students.  Questions about the Cuban Missile Crisis and the Berlin Wall were hard coded to CORRECT for all 15 students in the dataset.  The other 8 questions were given a radomized CORRECT or INCORRECT response for each student. The idea behind this is: would ChatGPT-4 correctly recognize that the Berlin Wall and the Cuban Missile Crisis likely didn't need to be in the lesson plan or needed to be emphasized less?

When the question `Write a lesson plan for what to teach based on the quiz results` was asked, I found that it still recommended a group activity discussing the Cuban Missile Crisis and the Berlin Wall, even though the test results showed 100% CORRECT responses on those two questions. So, this was a little disappointing at first.

However, when I asked it to `Analyze the data and look for recommendations on what I need to teach regarding the cold war` I found the response to be better.  It correctly excluded the Cold War and Berlin Wall from the response.  And, it even called out particularly problematic areas, saying things like `The Iron Curtain: The fifth question about the \"Iron Curtain\" had more incorrect answers than correct ones.`.

Then I asked a more metric based question about pass versus fail: `If passing the quiz means at least 60% answers correct, how many students passed the quiz versus failed the quiz?`. The system incorrectly answered that 10 students failed the quiz, which was disappointing. A pivot in Excel shows that only 6 students failed the quiz with the dataset.  However, the `What questions were answered 100% correct by all the students?` was answered correctly. The `Which question did the highest number of students answer wrong?` was also answered correcly.

Then I asked the system to `Using the question that the highest number of students answered wrong, write a lesson plan that specifically covers that question.`. Here is what it came up with:

```
Looking at the data, the question that the highest number of students answered wrong is: \"Which two major superpowers were the primary participants in the Cold War?\". 

Lesson Plan:

Title: The Cold War: The Clash of Superpowers

Objective: 
By the end of the lesson, students will be able to identify the two major superpowers that were the primary participants in the Cold War and understand their roles and ideologies.

Materials:
1. Textbook or online resources on the Cold War
2. Map of the world during the Cold War
3. Video clips or documentaries about the Cold War
4. Whiteboard and markers

Procedure:

1. Introduction (10 minutes)
   - Begin the lesson by asking students what they already know about the Cold War. Write their responses on the board.
   - Introduce the two superpowers involved in the Cold War: The United States and the Soviet Union.

2. Direct Instruction (20 minutes)
   - Provide a brief overview of the Cold War, emphasizing the roles of the United States and the Soviet Union.
   - Discuss the ideologies of each superpower (democracy and capitalism for the United States, communism for the Soviet Union).
   - Show the map of the world during the Cold War, pointing out the spheres of influence of each superpower.

3. Guided Practice (15 minutes)
   - Show a video clip or documentary about the Cold War, focusing on the roles of the United States and the Soviet Union.
   - Pause the video at key points to discuss and clarify.

4. Independent Practice (10 minutes)
   - Have students work individually or in pairs to answer a worksheet with questions about the two superpowers in the Cold War.

5. Closing (5 minutes)
   - Review the main points of the lesson.
   - Revisit the initial question: \"Which two major superpowers were the primary participants in the Cold War?\" and have students answer.

Homework:
Assign students to read a specific chapter or sections in their textbook or online resources that further discuss the roles of the United States and the Soviet Union in the Cold War.

Assessment:
Students' understanding will be assessed through their participation in class discussions, their answers to the worksheet, and their responses to the homework reading.
```

I found it intriguing that the system could indeed identify a specific subject area that most students had trouble with, and build a custom lesson plan specifically taylored to meet that area.

## Visual - Classroom Quiz Data Responses

![quiz responses](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/quiz-responses.png?raw=true)
![quiz lesson plan response](https://mckenzieservices.com/wp/wp-content/uploads/2023/09/quiz-lesson-plan-response.png?raw=true)

## Takeaways

One of the interesting findings is that how the data was sorted did significantly impact the quality of the response from Chat GPT-4.  For example, when 
I sorted the sales order data by order ID, I received back a more accurate response.  

This kind of technology will only get better and better.  I feel this is the tip of the iceberg of what can be done by analyzing data using natural language statements or questions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)


