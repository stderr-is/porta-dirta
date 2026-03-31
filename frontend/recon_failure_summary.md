# Shannon Scan Failure Analysis & Debugging Summary

## 1. Current Situation

The Shannon scan is currently failing during the **reconnaissance (`recon`) phase** with an **`OutputValidationError`**. This indicates that the reconnaissance agent is attempting to run, but the output it produces is not meeting Shannon's internal validation checks. The agent is repeatedly retrying, suggesting it's unable to generate valid results.

## 2. Setup Overview

*   **LLM Integration:** LiteLLM is configured as a proxy (`http://172.17.0.1:4000`) to connect Shannon to your local Ollama models.
*   **Proxy Configuration:** LiteLLM has been restarted with `drop_params=True` to handle unsupported parameters like `context_management`.
*   **Shannon Configuration:**
    *   Environment variables (`ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`) have been set to point to the LiteLLM proxy.
    *   `~/.shannon/config.toml` has been cleared to avoid provider conflicts.

## 3. Core Problem: Output Validation Failure

The `OutputValidationError` occurring during the "recon" phase, even with the LiteLLM proxy correctly configured, suggests that the reconnaissance agent is failing to produce its expected output file (`recon_deliverable.md`) in the required format or location. This is likely due to issues within the reconnaissance agent's execution, its interaction with the LLM, or the LLM's ability to generate the precise structured output Shannon's validation expects.

## 4. Potential Root Causes for Output Validation Failure

*   **LLM Output Formatting:** The LLM might be struggling to generate output in the exact Markdown structure required by Shannon's validation for reconnaissance reports.
*   **Prompt Complexity:** The reconnaissance prompt might be too complex or ambiguous, leading the LLM to produce output that doesn't precisely match validation rules.
*   **Agent Output Saving:** There could be an issue in how the reconnaissance agent attempts to save its output to `deliverables/recon_deliverable.md`.
*   **Model Capability:** The specific Ollama model might not be ideal for generating the highly structured output needed by the prompt.

## 5. Debugging Steps & Observations

*   **LiteLLM Proxy:** Resolved `UnsupportedParamsError` by setting `drop_params=True`.
*   **Shannon Startup:** The `start` command now completes successfully, indicating basic communication is established.
*   **Preflight Checks:** Appear to pass, allowing the scan to begin.
*   **Agent Execution:** `runReconAgent` is pending/retrying due to `OutputValidationError`.
*   **File Check:** `recon_deliverable.md` was found to be missing/empty, confirming the agent failed to produce its output.

## 6. Next Steps (Hypothetical if debugging were to continue)

*   **Prompt Refinement:** Simplify or clarify instructions in `recon.txt` for more robust structured output.
*   **Model Testing:** Experiment with different Ollama models that might excel at structured output generation.
*   **Agent Logic Review:** Investigate the `recon` agent's code for output saving mechanisms or potential execution errors.
*   **Validation Logic:** Understand the exact validation rules for `recon_deliverable.md`.

---
