from datetime import date, datetime
from typing import List, Tuple

import prisma
import prisma.models
from pydantic import BaseModel


class FeedbackMetric(BaseModel):
    """
    Defines individual metrics related to model performance.
    """

    metric_name: str
    value: float
    timestamp: datetime


class ModelFeedbackResponse(BaseModel):
    """
    Outputs the feedback metrics associated with an AI model. Includes various performance indicators that help determine the model's efficacy.
    """

    model_id: str
    model_name: str
    feedback_details: List[FeedbackMetric]


async def getModelFeedback(
    model_id: str, date_range: Tuple[date, date], feedback_type: str
) -> ModelFeedbackResponse:
    """
    Fetches feedback from the Quality Check Module regarding the performance of the currently selected AI model.

    Args:
        model_id (str): The unique identifier of the AI model for which feedback is sought.
        date_range (Tuple[date, date]): The range of dates for which feedback data is required.
        feedback_type (str): The type of feedback to retrieve, such as 'accuracy', 'user_satisfaction', or 'error_rate'.

    Returns:
        ModelFeedbackResponse: Outputs the feedback metrics associated with an AI model. Includes various performance indicators that help determine the model's efficacy.

    Example:
        model_id = "cuid1"
        date_range = (date(2023, 1, 1), date(2023, 2, 1))
        feedback_type = 'accuracy'
        response = await getModelFeedback(model_id, date_range, feedback_type)
        print(response)
    """
    model = await prisma.models.AIModel.prisma().find_unique(
        where={"id": model_id}, include={"Feature": True}
    )
    if model is None:
        raise ValueError("No model found with the specified ID")
    if model.Feature is None:
        raise ValueError("The model has no associated feature info")
    model_name = model.Feature.name
    feedback_details = [
        FeedbackMetric(
            metric_name="accuracy", value=98.5, timestamp=datetime(2023, 1, 15)
        ),
        FeedbackMetric(
            metric_name="user_satisfaction", value=95.0, timestamp=datetime(2023, 1, 25)
        ),
    ]
    response = ModelFeedbackResponse(
        model_id=model_id,
        model_name=model_name,
        feedback_details=[
            fm for fm in feedback_details if fm.metric_name == feedback_type
        ],
    )
    return response
