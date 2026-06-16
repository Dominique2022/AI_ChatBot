import os
from openai import OpenAI #openAI library for python, install with pip install openai
import tiktoken #library for tokenizing text, install with pip install tiktoken


api_key = os.getenv("TOGETHER_API_KEY").strip()

client = OpenAI(api_key=api_key,
                base_url="https://api.together.xyz/v1")  


#initialize the OpenAI client with the API key #Briefträger /Objekt
MODEL = "okengdjene_2517/meta-llama/Llama-3.3-70B-Instruct-Turbo-c9c851bc" #specify the model to use for generating responses
TEMPERATURE = 0.7 #Je höher die Temperatur, desto kreativer und unvorhersehbarer werden die Antworten.
MAX_TOKENS = 100 #maximum number of tokens in the generated response #Max number of words
SYSTEM_PROMPT = "You are a helpful assistant that provides accurate and concise answers to user questions." #define the system prompt for the chatbot
messages =[ #{role": "assistant", "content": "The capital of France is Paris."}, 
            {"role": "system", "content": SYSTEM_PROMPT
               }] #define the prompt for the chatbot, including system instructions and user input
TOKEN_LIMIT = 100


def chat(user_input):
    messages.append({"role": "user", "content": user_input}) #add the user input to the messages list
    
    response = client.chat.completions.create(
       model = MODEL,
       messages = messages ,
        temperature=TEMPERATURE, #Je höher die Temperatur, desto kreativer und unvorhersehbarer werden die Antworten. 
        max_tokens=MAX_TOKENS #maximum number of tokens in the generated response #Max number of words
           
    )  
      
    reply = response.choices[0].message.content.strip() #extract the generated response from the API response
    messages.append({"role": "assistant", "content": reply}) #add the generated response to the messages list
    
    return reply #return the generated response

while True:
    user_input = input("You: ") #get user input from the console
    if user_input.strip().lower() in {"exit", "quit"} : #check if the user wants to exit the chatbot
        print("Goodbye!")
        break
    answer = chat(user_input) #generate a response using the chat function
    print("you:",user_input)
    print("Bot:", answer) #print the generated response to the console

def get_encoding(model): #function to get the encoding for the specified model, with error handling for unknown models
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print("Model not found. Using cl100k_base encoding.")
        return tiktoken.get_encoding("cl100k_base")
    
    
ENCODING = get_encoding(MODEL) #get the encoding for the specified model     
 
def count_tokens(text):
    return len(ENCODING.encode(text)) #count the number of tokens in the given text using the specified encoding

def total_tokens_used(messages):
    try:
        return sum(count_tokens(message["content"]) for message in messages) #calculate the total number of tokens used in the messages list
    except Exception as e:
        print(f"Error counting tokens: {e}")
        return 0
    
    
def enforce_token_limit(messages, limit = TOKEN_LIMIT):
    try:
        while total_tokens_used(messages) > limit: #remove the oldest message from the messages list until the total number of tokens is within the specified limit
            if len(messages) <= 2:
                break  # Ensure we don't remove the system prompt or the most recent user message
            messages.pop(1)  # Remove the second message (the oldest user or assistant message)
    except Exception as e:
        print(f"Error enforcing token limit: {e}")
       
        
