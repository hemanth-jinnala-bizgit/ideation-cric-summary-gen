# #!/usr/bin/env python
# # src/hello_world/main.py
# import sys
# import warnings

# from datetime import datetime

# from hello_world.crew import HelloWorld

# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# # This main file is intended to be a way for you to run your
# # crew locally, so refrain from adding unnecessary logic into this file.
# # Replace with inputs you want to test with, it will automatically
# # interpolate any tasks and agents information

# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'AI LLMs',
#         'current_year': str(datetime.now().year)
#     }
    
#     try:
#         HelloWorld().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         HelloWorld().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         HelloWorld().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         HelloWorld().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")






# src/cricket_crew/main.py
import sys
import warnings
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from src.hello_world.crew import HelloWorld
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_inputs(match_id: str) -> Dict[str, Any]:
    """Get standardized inputs for the cricket crew"""
    return {
        'match_id': match_id,
        'timestamp': datetime.now().isoformat()
    }

def run(match_id: str):
    """Run the cricket analysis crew"""
    logger.info("Starting Cricket Match Analysis...")
    
    if not match_id:
        raise ValueError("Match ID is required")
    
    inputs = get_inputs(match_id)
    logger.info(f"Analyzing match ID: {match_id}")
    
    try:
        crew_instance = HelloWorld()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        logger.info("Cricket analysis completed successfully")
        logger.info(f"Results available in crew output")
        
        return result
        
    except Exception as e:
        logger.error(f"Cricket analysis failed: {str(e)}")
        raise Exception(f"An error occurred while analyzing the match: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        match_id = sys.argv[1]
        run(match_id)
    else:
        # Default match ID for testing
        run("105778")