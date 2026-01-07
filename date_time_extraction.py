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


text="""Dear Students,
As part of a new academic initiative, we have developed a feedback portal to collect course feedback from students.

An email containing your login credentials (username and password), along with the link to access the portal, will be sent to you shortly. Please log in using the provided credentials, change your password upon first login, and submit feedback for the respective courses and faculty members.

A user manual is attached to this email for your reference. In case you face any technical issues or have queries related to the portal, please write to portal.support@iiits.in.

Since this is the first time feedback is being collected through this portal, your kind cooperation and support are highly appreciated. Please be assured that the feedback process is completely anonymous. We encourage you to provide honest feedback and constructive suggestions to help us continuously improve the quality of our academic programs.

Thank you for your valuable time and support. Submissions wil close within 15 days .
Regards, 
A.Suneetha 
Assistant Manager
Academic Office 
Indian Institute of Information Technology Sri City"""

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    max_new_tokens=300,
)


model = ChatHuggingFace(llm=llm, temperature=0)


class EventDate(BaseModel):
    role: Optional[Literal["start", "end", "single"]] = Field(
        description="Use start/end if applicable, otherwise single"
    )
    date: datetime.date = Field(description="Date in YYYY-MM-DD format")
    time: Optional[datetime.time] = Field(
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

1. Extract ONLY dates that are explicitly mentioned or expressed as
   relative dates (e.g., tomorrow, this Saturday, next Monday, in 30 days).
2. Resolve all relative dates using TODAY'S DATE.

--- DEADLINE LOGIC (VERY IMPORTANT) ---
3. If the text contains deadline or completion phrases such as:
   "complete by", "submit by", "deadline", "closes by", "will close",
   then:
   a. Output EXACTLY TWO events ONLY:
      - role = "start" → TODAY'S DATE
      - role = "end" → resolved deadline date
   b. DO NOT extract, infer, or include ANY other dates.

4. If a date is mentioned WITHOUT any deadline/completion wording,
   extract ONLY that date with role = "single".
   Do NOT add a start date in this case.
5.If the deadline is already passed then it should alert the user that the deadline is already passed
--- TIME HANDLING ---
5. If time is explicitly mentioned, extract it.
6. If time is NOT mentioned for an extracted date, set time to 10:00 AM.

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

result2=chain2.invoke({'email_text':text})

# print(result2)
print(dict(result2))
# print(type(result2))




