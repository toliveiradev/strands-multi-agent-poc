import os
import logging
from pythonjsonlogger import jsonlogger
from strands import Agent, tool
from strands.models.openai import OpenAIModel

logger = logging.getLogger("Orchestrator")
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

MEDIA_STORE = {
    "ep_402": {
        "metadata": {
            "show_id": "tech_audio_talk",
            "duration_seconds": 3450,
            "demographic_targets": ["18-24", "25-34"],
            "peak_listen_time": "Morning Commute",
            "historical_engagement_score": 0.88,
            "sponsors": ["TechAudio Inc", "StreamCloud"]
        },
        "transcript_preview": "Welcome to Tech Audio Talk. Today we discuss the impact of AI on music production and audio engineering...",
        "content_flags": ["technology", "ai", "audio_industry"]
    }
}

@tool
def get_podcast_context(episode_id: str) -> dict:
    """Retrieves podcast metadata and transcripts from internal catalog."""
    logger.info("Tool Invocation: get_podcast_context", extra={"episode_id": episode_id})
    return MEDIA_STORE.get(episode_id, {"error": "Episode not found", "episode_id": episode_id})

def initialize_llm():
    endpoint = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name = os.getenv("LOCAL_MODEL_NAME", "llama3.2:3b")
    logger.info("Initializing Local LLM via Ollama", extra={"endpoint": endpoint, "model": model_name})
    
    return OpenAIModel(
        model_id=model_name,
        client_args={
            "base_url": f"{endpoint}/v1",
            "api_key": "ollama"
        }
    )

def execute_pipeline(episode_id: str):
    logger.info("Pipeline Started: Multi-Agent Supervisor Workflow", extra={"episode_id": episode_id})
    
    llm = initialize_llm()

    researcher = Agent(
        name="Media_Researcher",
        model=llm,
        system_prompt="You are a data retrieval specialist. Call get_podcast_context to retrieve episode data.",
        tools=[get_podcast_context]
    )

    evaluator = Agent(
        name="Brand_Safety_Evaluator",
        model=llm,
        system_prompt="""You are a brand safety and audience alignment auditor.
        Evaluate social media copies. Respond with a JSON object:
        {"approved": true/false, "score": 0.0-1.0, "feedback": "reasoning"}"""
    )

    supervisor = Agent(
        name="Workflow_Supervisor",
        model=llm,
        system_prompt="""You coordinate content generation and validation.
        1. Ask Media_Researcher for episode details.
        2. Write an engaging social media post targeted at young adults (18-34).
        3. Submit the copy to Brand_Safety_Evaluator for audit.
        Provide the final output with the approved copy and evaluator comments.""",
        tools=[researcher, evaluator]
    )

    logger.info("Agent State: Supervisor delegating tasks to workers...")
    response = supervisor(f"Process episode '{episode_id}' and generate verified social copy.")
    
    logger.info("Pipeline Completed: Verified payload generated successfully")
    print("\n================ FINAL VERIFIED PAYLOAD ================")
    print(response)
    print("========================================================\n")

if __name__ == "__main__":
    execute_pipeline("ep_402")