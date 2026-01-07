from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableSequence,RunnableLambda
from pydantic import BaseModel,Field
from typing import Literal,Optional,List
import datetime


load_dotenv()

from datetime import date 
today =date.today().isoformat()



#STEP-01                                                     """URGENCY CLASSFICATION"""





llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    max_new_tokens=300,
)


model = ChatHuggingFace(llm=llm, temperature=0)

class Sentiment(BaseModel):
    urgency:Literal["high","moderate","low"] =Field(description="Analyze the  urgency of reply for this email as high,moderate or low")

pyparser=PydanticOutputParser(pydantic_object=Sentiment)

prompt1=PromptTemplate(template="""
                       Todays date is {date}
                       analyze this email text  {email_text} and dAnalyze the following email and determine the urgency of reply
based on:
1. Proximity of the deadline(if the deadline falls 2 or 3 days from now label it as high urgency,if the deadline is within a week make it as moderate and rest it as low )
2. Required action by the recipient
3. Consequences of missing the deadline
4. If nothing about deadline  is mentioned then the default output should be low urgency                        \n {format_instruction}""",
                        input_variables=['email_text','date'],
                        partial_variables={'format_instruction':pyparser.get_format_instructions()}

                        )

chain1=prompt1|model|pyparser

def classify_urgency(email_text: str) -> str:
    today = datetime.date.today().isoformat()
    result = chain1.invoke({
        "email_text": email_text,
        "date": today
    })
    return result.urgency

# result=chain1.invoke({'email_text':text,'date':today})
# print(dict(result)['urgency'])


#STEP-2                    """ DATE,TIME AND TASK NAME EXTRACTION """


# from pydantic import field_validator

# class EventDate(BaseModel):
#     role: Optional[Literal["start", "end", "single"]]
#     date: datetime.date
#     time: Optional[str]

#     @field_validator("time", mode="before")
#     @classmethod
#     def fix_null_time(cls, v):
#         if v is None:
#             return None
#         if isinstance(v, str) and v.strip().lower() == "null":
#             return None
#         return v

class EventDate(BaseModel):
    role: Optional[Literal["start", "end", "single"]] = Field(
        description="Use start/end if applicable, otherwise single"
    )
    date: datetime.date = Field(description="Date in YYYY-MM-DD format")
    time: Optional[str] = Field(
        description="Time in HH:MM (24-hour). Optional"
    )

class Extraction(BaseModel):
    task_name: str = Field(description="Short description of the task")
    events: List[EventDate] = Field(description="List of extracted dates/times")

pyparser2=PydanticOutputParser(pydantic_object=Extraction)

prompt2 = PromptTemplate(
    template="""
You are a STRICT information extraction system.

TODAY'S DATE: {today}

TASK:
Extract task-related dates and times from the email.

RULES (MUST FOLLOW EXACTLY):

--- DEADLINE LOGIC (VERY IMPORTANT) ---
1. If the text contains deadline or completion phrases such as:
   "complete by", "submit by", "deadline", "closes by", "will close",
   then:
   a. Output EXACTLY TWO events ONLY:
      - role = "start" → TODAY'S DATE
      - role = "end" → resolved deadline date
   b. DO NOT extract, infer, or include ANY other dates.

2. Extract ONLY dates that are explicitly mentioned or expressed as
   relative dates (e.g., tomorrow, this Saturday, next Monday, in 30 days).
3. Resolve all relative dates using TODAY'S DATE.



4. If a date is mentioned WITHOUT any deadline/completion wording,
   extract ONLY that date with role = "single".
   Do NOT add a start date in this case.

--- TIME HANDLING ---
5. If time is explicitly mentioned, extract it.
6. If time is NOT explicitly mentioned, return time as null (JSON null).
   Do NOT infer or default time.
- Use null without quotes for missing fields.


--- OUTPUT RULES ---
7. Dates MUST be in YYYY-MM-DD format.
8. Times MUST be in HH:MM (24-hour) format.
9. Output ONLY valid JSON matching the schema.
10. Do NOT include explanations or extra text.

EMAIL TEXT:
{email_text}

{format_instructions}
""",
    input_variables=["email_text"],
    partial_variables={
        "today": today,
        "format_instructions": pyparser2.get_format_instructions()
    }
)


chain2=prompt2|model|pyparser2

def extract_events_from_email(email_text: str) -> Extraction:
    today = datetime.date.today().isoformat()
    result = chain2.invoke({
        "email_text": email_text
    })
    return result


# result2=chain2.invoke({'email_text':text})

# # print(result2)
# print(dict(result2))
# # print(type(result2))

