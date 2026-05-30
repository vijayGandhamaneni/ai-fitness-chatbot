from pydantic import BaseModel, Field
from typing import List

# Individual Chat Message

class Message(BaseModel):

    role: str
    content: str

# Chat Request Model

class ChatRequest(BaseModel):

    message: str

    chat_history: List[Message] = Field(
        default_factory=list
    )