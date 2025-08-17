import os
import sys
from typing import Iterator
from google import genai
from google.genai import types
from agentConversation import AgentConversation
import toolsWrapper

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan using the included tools. You can:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

WORKING_DIR = "./calculator"

class Agent:
    def __init__(self) :
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        self.convo = AgentConversation()
        self.isVerbose = '--verbose' in sys.argv
        self.promptConfig = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=toolsWrapper.tools
        )
        self.workingDir = WORKING_DIR

    def postPrompt(self, prompt: str) :
        if self.isVerbose : print(f"User prompt: {prompt}")
        isIterating = True
        count = 0
        res = None
        while isIterating:
            count = count + 1
            res = self._genContent(prompt)
            self._handleGenContentResponse(res)

            #if response has text, assume it's done
            if (res.text and not res.function_calls) or count > 20: isIterating = False

        return res.text;

    def _genContent(self, prompt: str) -> types.GenerateContentResponse :
        self.convo.addTextContent(prompt, AgentConversation.ContentRole.USER)
        return self.client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = self.convo.contents,
            config = self.promptConfig
        )
    
    def _handleGenContentResponse(self, res: types.GenerateContentResponse) :
        self.convo.addContent(res.candidates[0].content)
        self._printContentResponse(res)
        if res.function_calls:
            for call in res.function_calls:
                self._callFunction(call)
    
    def _callFunction(self, funcCall: types.FunctionCall):
        funcCall.args['working_directory'] = self.workingDir
        if self.isVerbose : 
            print(f"Calling function: {funcCall.name}({funcCall.args})")
        else :
            print(f" - Calling function: {funcCall.name}")
        
        res = None
        try:    
            res = {"result": toolsWrapper.runFunc(funcCall.name, funcCall.args)}
            if self.isVerbose: print(f" -> {res["result"]}")
        except Exception as e:
            res = {"error": e}
            if self.isVerbose: print(f" -> {res["error"]}")


        self.convo.addFuncResultContent(funcCall.name, res, AgentConversation.ContentRole.USER)
            
    def _printContentResponse(self, content: types.GenerateContentResponse):
        if self.isVerbose : 
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count} \n")
        print(content.text)
        # for function_call in content.function_calls :
        #     print(f"Calling function: {function_call.name}({function_call.args})")
        print('\n\n')

    # def _genContentStream(self, client: genai.Client, prompt: str) -> None :
    #     res = client.models.generate_content_stream(
    #         model="gemini-2.0-flash-001",
    #         contents=prompt,
    #         config = self.promptConfig
    #     )
    #     self._readChunks(res)

    # def _readChunks(self, res: Iterator[types.GenerateContentResponse]) -> None:
    #     i = 0
    #     for chunk in res:
    #         print(f"chunk {i}")
    #         i += 1
    #         if self.isVerbose : self._printContentResponse(chunk)
    

