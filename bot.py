import os
from openai import OpenAI #openAI library for python, install with pip install openai


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
    print("Bot:", answer) #print the generated response to the console