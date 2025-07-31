from langchain_community.chat_models import BedrockChat

class SafeBedrockChatLLM(BedrockChat):
    def __deepcopy__(self, memo):
        # Prevent deepcopying this object
        return self

    def __getstate__(self):
        # Prevent JSON serialization error
        return {
            "model_id": self.model_id,
            "region_name": getattr(self, "region_name", "us-east-1")
        }

    def __setstate__(self, state):
        # Restore minimal state if needed
        self.model_id = state["model_id"]
        self.region_name = state["region_name"]
