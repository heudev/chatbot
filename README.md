## Discord ChatBot

- This project is a Python-based Discord chatbot that uses Jaccard similarity to respond to user input. The bot is designed to respond to user input based on keywords defined in a ```conversation.json``` file. If the user's input matches any of the ```keywords```, the bot will randomly select a response from the ```answers``` field in the file.

- The Jaccard similarity metric is used to determine how closely the user's input matches the keywords in the ```conversation.json``` file. The Jaccard similarity is a measure of the similarity between two sets of data, and it ranges from 0 to 1. A value of 0 indicates no similarity between the sets, while a value of 1 indicates perfect similarity.

- To adjust the bot's response to user input, you can increase or decrease the Jaccard similarity threshold. If the threshold is set high, the bot will only respond to user input that closely matches the keywords. If the threshold is set low, the bot will respond to a wider range of user input.


## Run the project on your computer

Clone the project

```bash
  git clone https://github.com/heudev/chatbot.git
```

Install dependencies

```bash
  pip install discord flask 
```

Run the bot

```bash
  python3 main.py
```

  
