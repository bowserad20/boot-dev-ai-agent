from enum import Enum
from google import genai
from google.genai import types

class AgentConversation:
    def __init__(self) :
        self.contents : list[types.Content] = []

    def addTextContent(self, text: str, role: str):
        content = types.Content(parts = [types.Part(text=text)], role = role)
        self.contents.append(content)

    def addFuncResultContent(self, funcName: str, funcResponse: dict[str, any], role: str):
        content = types.Content(
            parts = [types.Part.from_function_response(name=funcName, response=funcResponse)], 
            role = role
        )
        self.contents.append(content)
    
    def addContent(self, content : types.Content):
        self.contents.append(content)

    class ContentRole(Enum):
        USER = 'user'
        MODEL = 'model'
