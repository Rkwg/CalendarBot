from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dateparser import parse
from calendar_utils import get_availability, book_event
from datetime import timedelta
import pytz
import os
import dateparser
from dotenv import load_dotenv

load_dotenv()
IST = pytz.timezone("Asia/Kolkata")
llm = ChatOpenAI(
    temperature=0,
    model="mistralai/mistral-7b-instruct",  
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

prompt = PromptTemplate.from_template("""
You are an AI assistant that helps users book calendar appointments. 
Extract datetime and intent, then suggest available slots or book the meeting.
Input: {input}
""")

chain = LLMChain(llm=llm, prompt=prompt)

def process_input(user_input):
    _ = chain.run(input=user_input) 
    time = dateparser.parse(
        user_input,
        settings={
            "PREFER_DATES_FROM": "future",             
            "TIMEZONE": "Asia/Kolkata",                
            "RETURN_AS_TIMEZONE_AWARE": True           
        }
    )
    if not time:
        return "I couldn't understand the time. Could you try something like 'tomorrow at 4pm' or 'next Monday at 10am'?"
    
    time = time.astimezone(IST)

    try:
        start = time
        end = start + timedelta(hours=1)
        events = get_availability(start, end)
        if events:
            return f"You're not free then. Try another time."
        link = book_event("User Meeting", start, end)
        return f"✅ Your meeting is booked! Here is the link: {link}"
    except Exception as e:
        return f"⚠️ Internal Error: {str(e)}"
    
