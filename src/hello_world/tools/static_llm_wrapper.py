import copy
from langchain_community.chat_models import BedrockChat

class SafeBedrockChatLLM(BedrockChat):
    def __deepcopy__(self, memo):
        # Prevent deepcopy on this object
        return self
