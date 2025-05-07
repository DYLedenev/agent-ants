from unittest.mock import patch
from agents.base import Queen, Agent
from core.task import Task

@patch("tools.classifier.generate")
@patch("core.llm.generate")
def test_orchestrate_healthcare_pipeline(mock_generate_llm, mock_classify):
    # === SETUP ===
    queen = Queen("queen")
    agents = [
        Agent(name="researcher", config={"task_type": "research"}),
        Agent(name="summarizer", config={"task_type": "summarize"}),
        Agent(name="analyst", config={"task_type": "analysis"}),
    ]

    task = Task(content="Plan and summarize a mini research report about how AI is used in healthcare, then extract key risks and suggest how to mitigate them.")

    # === CLASSIFIER always returns the following sequence of types ===
    mock_classify.side_effect = (
        ["research", "summarize", "analysis", "analysis"] * 5  # safety net
    )

    # === LLM.generate responses ===
    def fake_generate(prompt, system=None):
        if prompt.strip().startswith("Split the following task"):
            return """
            Research how AI is currently used in healthcare.
            Summarize the main applications of AI in diagnostics and patient care.
            Identify potential risks of using AI in medicine.
            Suggest ways to mitigate these risks.
            """
        elif prompt.strip().startswith("Create a concise executive summary"):
            return "AI in healthcare improves diagnostics and patient monitoring, but raises concerns like bias and data privacy."
        else:
            return f"[MOCKED RESPONSE for: {prompt[:40]}...]"

    mock_generate_llm.side_effect = fake_generate

    # === ACT ===
    result = queen.orchestrate(task, agents)
    real_results = {
        k: v for k, v in result["results"].items()
        if not k.startswith("<") and not k.endswith(">") and not k.startswith("[") and not k.endswith("]")
    }
    # === ASSERT ===
    assert isinstance(real_results, dict)
    assert "results" in real_results and isinstance(real_results["results"], dict)
    assert "summary" in real_results
    assert "AI in healthcare" in real_results["summary"]
    assert len(real_results["results"]) == 4
    assert all("MOCKED RESPONSE" in v for k, v in result["results"].items() if not k.startswith("<"))
