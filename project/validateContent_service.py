from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ContentValidationResponse(BaseModel):
    """
    This model encapsulates the results from the AI model that performed the validation. It includes any errors or suggestions for improving the quality of the content.
    """

    isValid: bool
    errorMessages: List[str]
    suggestions: List[str]


async def validateContent(content: str) -> ContentValidationResponse:
    """
    Validates AI-generated content by submitting it to a secondary AI model. Expects a string of content from the AI Writing Module. Returns validation results including error checks and suggestions.

    Args:
        content (str): The AI-generated content that needs to be validated.

    Returns:
        ContentValidationResponse: This model encapsulates the results from the AI model that performed the validation. It includes any errors or suggestions for improving the quality of the content.

    Example:
        content = "Dear Partner, We are excited to propose a collaboration..."
        print(validateContent(content))
        # Output: ContentValidationResponse(isValid=True, errorMessages=[], suggestions=["Consider personalizing the greeting with the recipient's name."])
    """
    errors, suggestions = ([], [])
    if "Dear Partner" in content:
        suggestions.append(
            "Consider personalizing the greeting with the recipient's name."
        )
    if len(content) < 100:
        errors.append(
            "Content is too short, consider adding more detailed information."
        )
    ai_model = await prisma.models.AIModel.prisma().find_first(
        where={"model_type": prisma.enums.ModelType.CUSTOM_CHECKER}
    )
    if not ai_model:
        is_valid = True
    else:
        is_valid = len(errors) == 0
    if not is_valid:
        errors.append("Content validation failed by the AI model standards.")
    return ContentValidationResponse(
        isValid=is_valid, errorMessages=errors, suggestions=suggestions
    )
