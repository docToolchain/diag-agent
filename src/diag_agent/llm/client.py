"""LLM client for diagram generation via LiteLLM."""

from typing import Any
import re
import litellm


class LLMGenerationError(Exception):
    """Exception raised when LLM diagram generation fails.
    
    This wraps LLM API errors with additional context about
    the provider, model, and error details.
    """
    pass


class LLMClient:
    """Client for interacting with LLM providers via LiteLLM.

    Supports multiple providers (Anthropic, OpenAI, local models)
    through unified LiteLLM interface.
    """

    def __init__(self, settings: Any) -> None:
        """Initialize LLM client with settings.

        Args:
            settings: Application settings (Settings instance)
        """
        self.settings = settings

    def _strip_markdown_code_blocks(self, content: str) -> str:
        """Strip markdown code blocks from LLM response.

        Removes ```language ... ``` or ``` ... ``` blocks and returns clean code.

        Args:
            content: Raw LLM response possibly containing markdown code blocks

        Returns:
            Clean diagram code without markdown formatting
        """
        # Pattern: ```[optional language]\n<code>\n```
        # This handles both ```plantuml and ``` variants
        pattern = r'^```[\w]*\n(.*?)\n```$'
        match = re.match(pattern, content.strip(), re.DOTALL)
        
        if match:
            return match.group(1)
        
        # No markdown blocks found - return as is
        return content

    def generate(self, prompt: str) -> str:
        """Generate diagram source code from prompt.

        Args:
            prompt: Natural language description and instructions for diagram

        Returns:
            Generated diagram source code

        Raises:
            LLMGenerationError: If LLM API call fails
        """
        # Build model string: provider/model (e.g., "anthropic/claude-sonnet-4")
        model = f"{self.settings.llm_provider}/{self.settings.llm_model}"

        try:
            # Call LiteLLM completion API with system message for clean output
            response = litellm.completion(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "Return only the diagram code. No markdown formatting. No explanations."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract generated content from response
            raw_content = response.choices[0].message.content
            
            # Strip markdown code blocks for clean diagram code
            return self._strip_markdown_code_blocks(raw_content)

        except Exception as e:
            # Convert any LLM errors to custom exception with context
            raise LLMGenerationError(
                f"LLM generation failed for model '{model}': {str(e)}"
            ) from e

    def vision_analyze(self, image_bytes: bytes, prompt: str) -> str:
        """Analyze diagram image using vision-capable LLM.

        Args:
            image_bytes: PNG image bytes to analyze
            prompt: Analysis instructions (e.g., "Evaluate layout quality")

        Returns:
            Design feedback string from LLM

        Raises:
            LLMGenerationError: If LLM API call fails
        """
        import base64

        # Convert PNG bytes to base64 data URL
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        data_url = f"data:image/png;base64,{base64_image}"

        # Build model string: provider/model (e.g., "anthropic/claude-3-7-sonnet-latest")
        model = f"{self.settings.llm_provider}/{self.settings.llm_model}"

        try:
            # Call LiteLLM completion API with vision message structure
            response = litellm.completion(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": data_url
                                }
                            }
                        ]
                    }
                ]
            )

            # Extract design feedback from response
            return response.choices[0].message.content

        except Exception as e:
            # Convert any LLM errors to custom exception with context
            raise LLMGenerationError(
                f"LLM vision analysis failed for model '{model}': {str(e)}"
            ) from e

    def validate_description(self, description: str, diagram_type: str) -> tuple[bool, str | None]:
        """Validate diagram description for completeness and consistency.

        Args:
            description: Natural language description of diagram
            diagram_type: Type of diagram (plantuml, bpmn, etc.)

        Returns:
            Tuple of (is_valid, questions):
            - (True, None): Description is valid
            - (False, questions_str): Description invalid, questions contains numbered issues

        Note:
            On API errors, returns (True, None) to allow workflow to continue (fail-safe).
        """
        # Build model string
        model = f"{self.settings.llm_provider}/{self.settings.llm_model}"

        # Validation prompt
        validation_prompt = f"""You are a diagram description validator. Analyze the given description for a {diagram_type} diagram.

Check for:
1. Completeness: Are essential elements specified?
2. Consistency: Are there contradictions?
3. Clarity: Is the description unambiguous?

Only flag actual problems that would prevent generating a useful diagram. Be lenient - minor imperfections are acceptable.

Response format:
- If valid: Return exactly "VALID"
- If invalid: Return "INVALID" on first line, then numbered questions on separate lines

Example invalid response:
INVALID
1. Which type of BPMN diagram is needed? (process/collaboration/choreography)
2. Who performs the "approval step"? Specify role or system name.

Description to validate:
{description}"""

        try:
            # Call LLM for validation
            response = litellm.completion(
                model=model,
                messages=[
                    {"role": "user", "content": validation_prompt}
                ]
            )

            # Parse response
            content = response.choices[0].message.content.strip()
            
            if content.startswith("VALID"):
                return (True, None)
            elif content.startswith("INVALID"):
                # Extract questions (everything after "INVALID\n")
                lines = content.split("\n", 1)
                if len(lines) > 1:
                    questions = lines[1].strip()
                    return (False, questions)
                else:
                    # Malformed response - fail-safe to valid
                    return (True, None)
            else:
                # Unexpected format - fail-safe to valid
                return (True, None)

        except Exception:
            # API error or other failure - fail-safe to valid
            # This allows workflow to continue even if validation service is down
            return (True, None)
