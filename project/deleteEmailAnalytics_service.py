import prisma
import prisma.models
from pydantic import BaseModel


class DeleteEmailAnalyticsResponse(BaseModel):
    """
    Confirmation of deletion of email analytics data; includes the status of the deletion operation.
    """

    status: str
    message: str


async def deleteEmailAnalytics(emailId: str) -> DeleteEmailAnalyticsResponse:
    """
    Removes specified email's analytics data from the system. This might be necessary when data is outdated or if the email analysis was created in error. It helps keep the analytics database manageable and relevant.

    Args:
        emailId (str): The unique identifier of the email whose analytics data is to be deleted.

    Returns:
        DeleteEmailAnalyticsResponse: Confirmation of deletion of email analytics data; includes the status of the deletion operation.

    Example:
        emailId = 'abc123'
        response = await deleteEmailAnalytics(emailId)
        > {'status': 'success', 'message': 'Email analytics data successfully deleted.'}
    """
    await prisma.models.CampaignMetric.prisma().delete_many(
        where={"emailCampaignId": emailId}
    )
    response = DeleteEmailAnalyticsResponse(
        status="success", message="Email analytics data successfully deleted."
    )
    return response
