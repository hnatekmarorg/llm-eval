import argparse

from loguru import logger
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


def log_retry(retry_state):
    """Callback function to log before a retry."""
    logger.warning(
        "Retrying '{}' (attempt {}): {}",
        retry_state.fn.__name__,
        retry_state.attempt_number,
        retry_state.outcome.exception()
    )

def is_transient_error(e: Exception) -> bool:
    """Determine if an exception should trigger a retry."""
    transient_exceptions = (
        ConnectionError,
        TimeoutError,
    )
    return isinstance(e, transient_exceptions)

@retry(
    retry=retry_if_exception_type(),
    stop=stop_after_attempt(500),
    wait=wait_exponential(multiplier=1, max=10),
    before_sleep=log_retry,
    reraise=True
)
def run_prompt(agent: Agent, prompt_file: str) -> str:
    with open(prompt_file, "r") as f:
        result = agent.run_sync(f.read())
        return result.output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('model')
    args = parser.parse_args()
    logger.info("Starting evaluation with {}", args.model)
    model = OpenAIChatModel(
        model_name=args.model,
        provider=OpenAIProvider(
            base_url=args.url
        )
    )
    agent = Agent(
        model=model,
        system_prompt=""
    )

    import glob
    for prompt in sorted(glob.glob("tests/*")):
        logger.info("Evaluating {}", prompt)
        result = run_prompt(agent, prompt)
        with open(f"output/{args.model}-{prompt.replace('tests/', '')}.md", "w+") as f:
            f.write(result)


if __name__ == "__main__":
    main()
