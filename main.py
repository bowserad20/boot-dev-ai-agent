import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import Iterator
from agent import Agent
from agentConversation import AgentConversation
def main():
    load_dotenv()
    agent = Agent()
    agent.postPrompt(getPromptFromArgs())

def getPromptFromArgs() -> str :
    if (len(sys.argv) < 2) : 
        print('no prompt provided')
        exit(1)
    return sys.argv[1]

if __name__ == "__main__":
    main()
