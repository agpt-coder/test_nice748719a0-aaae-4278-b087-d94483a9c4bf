import io
import logging
from contextlib import asynccontextmanager

import prisma
import project.createContentRequest_service
import project.createDraft_service
import project.createEmailAnalysis_service
import project.createTemplate_service
import project.deleteDraft_service
import project.deleteEmailAnalytics_service
import project.deleteGeneratedContent_service
import project.deleteTemplate_service
import project.deleteValidation_service
import project.fetchGeneratedContent_service
import project.getAnalytics_service
import project.getDraftById_service
import project.getDrafts_service
import project.getEmailPerformance_service
import project.getModelFeedback_service
import project.getTemplate_service
import project.getValidationStatus_service
import project.listModels_service
import project.listTemplates_service
import project.listValidations_service
import project.selectModel_service
import project.updateDraft_service
import project.updateEmailAnalysis_service
import project.updateGeneratedContent_service
import project.updateTemplate_service
import project.updateValidation_service
import project.validateContent_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, StreamingResponse
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="test_nice",
    lifespan=lifespan,
    description="""a project that allows users to write B2B and B2C cold emails utilizing AI. In the program use LiteLLM so I can call multiple models like gpt-4-turbo and another model for checking output of gpt-4-turbo""",
)


@app.patch(
    "/ai-writing/content/{contentId}",
    response_model=project.updateGeneratedContent_service.ContentUpdateResponse,
)
async def api_patch_updateGeneratedContent(
    contentId: str, newContent: str, newStatus: Optional[DraftStatus]
) -> project.updateGeneratedContent_service.ContentUpdateResponse | Response:
    """
    Updates a specific generated content. This endpoint is necessary when post-creation edits are required by the users. Only allowed before the content is sent to Quality Check Module. Returns the updated status of the content.
    """
    try:
        res = project.updateGeneratedContent_service.updateGeneratedContent(
            contentId, newContent, newStatus
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/templates/{templateId}",
    response_model=project.getTemplate_service.GetTemplateResponse,
)
async def api_get_getTemplate(
    templateId: str,
) -> project.getTemplate_service.GetTemplateResponse | Response:
    """
    Fetches a specific template by its unique identifier, 'templateId'. The response includes complete details of the template such as title, content, and creation date. Useful for template previews or editing.
    """
    try:
        res = await project.getTemplate_service.getTemplate(templateId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/drafts/{draftId}", response_model=project.deleteDraft_service.DeleteDraftResponse
)
async def api_delete_deleteDraft(
    draftId: str,
) -> project.deleteDraft_service.DeleteDraftResponse | Response:
    """
    Deletes a specific draft identified by draftId. This operation is irreversible and used for drafts that are no longer needed or were created in error. Success response indicates whether the draft was successfully deleted. Response: {deleted: boolean}.
    """
    try:
        res = await project.deleteDraft_service.deleteDraft(draftId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/quality-check/delete/{validationId}",
    response_model=project.deleteValidation_service.DeleteValidationResponse,
)
async def api_delete_deleteValidation(
    validationId: str,
) -> project.deleteValidation_service.DeleteValidationResponse | Response:
    """
    Deletes a specific validation request identified by {validationId}. This is typically allowed for users who have the authority to manage or need to clear outdated validation tasks.
    """
    try:
        res = await project.deleteValidation_service.deleteValidation(validationId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/drafts", response_model=project.getDrafts_service.GetDraftsResponse)
async def api_get_getDrafts(
    request: project.getDrafts_service.GetDraftsRequest,
) -> project.getDrafts_service.GetDraftsResponse | Response:
    """
    Retrieves a list of all editable drafts generated by the AI Writing Module. Each draft includes unique identifiers and editable content fields, making it easier for users to select and modify. Expected response structure: [{draftId: string, content: string, editable: boolean}].
    """
    try:
        res = await project.getDrafts_service.getDrafts(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/ai-writing/content/{contentId}",
    response_model=project.deleteGeneratedContent_service.DeleteContentResponse,
)
async def api_delete_deleteGeneratedContent(
    contentId: str,
) -> project.deleteGeneratedContent_service.DeleteContentResponse | Response:
    """
    Deletes a specific generated content. This is crucial for managing data privacy and storage. Returns confirmation of the deletion.
    """
    try:
        res = await project.deleteGeneratedContent_service.deleteGeneratedContent(
            contentId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/analytics/emails/{emailId}",
    response_model=project.deleteEmailAnalytics_service.DeleteEmailAnalyticsResponse,
)
async def api_delete_deleteEmailAnalytics(
    emailId: str,
) -> project.deleteEmailAnalytics_service.DeleteEmailAnalyticsResponse | Response:
    """
    Removes specified email's analytics data from the system. This might be necessary when data is outdated or if the email analysis was created in error. It helps keep the analytics database manageable and relevant.
    """
    try:
        res = await project.deleteEmailAnalytics_service.deleteEmailAnalytics(emailId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/templates/{templateId}",
    response_model=project.deleteTemplate_service.DeleteTemplateResponse,
)
async def api_delete_deleteTemplate(
    templateId: str,
) -> project.deleteTemplate_service.DeleteTemplateResponse | Response:
    """
    Deletes the specified template by its 'templateId'. This is irreversible and typically restricted to high-level roles. On successful deletion, it usually returns HTTP 204 with no content.
    """
    try:
        res = await project.deleteTemplate_service.deleteTemplate(templateId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/templates/{templateId}",
    response_model=project.updateTemplate_service.UpdateTemplateResponse,
)
async def api_put_updateTemplate(
    templateId: str, title: str, content: str, category: Optional[str]
) -> project.updateTemplate_service.UpdateTemplateResponse | Response:
    """
    Updates an existing email template identified by 'templateId'. This can modify the template's content, title, and other properties. Requires a JSON body with the updated attributes. The endpoint provides an updated template object as response.
    """
    try:
        res = await project.updateTemplate_service.updateTemplate(
            templateId, title, content, category
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/drafts/{draftId}", response_model=project.getDraftById_service.FetchDraftResponse
)
async def api_get_getDraftById(
    draftId: str,
) -> project.getDraftById_service.FetchDraftResponse | Response:
    """
    Fetches a specific draft by its unique identifier. This route is used to retrieve detailed information about a draft to allow for focused editing. Response includes fields like content, status, and last edited timestamp. Expected output: {draftId: string, content: string, status: string, lastEdited: timestamp}.
    """
    try:
        res = await project.getDraftById_service.getDraftById(draftId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/analytics/emails/{emailId}",
    response_model=project.getEmailPerformance_service.EmailAnalyticsResponse,
)
async def api_get_getEmailPerformance(
    emailId: str,
) -> project.getEmailPerformance_service.EmailAnalyticsResponse | Response:
    """
    Provides detailed analytics for a specific email. It fetches data such as the number of opens, clicks, and conversions directly related to the individual email ID. This detailed view helps in understanding the effectiveness of single email dispatches.
    """
    try:
        res = await project.getEmailPerformance_service.getEmailPerformance(emailId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/models", response_model=project.listModels_service.GetModelsResponse)
async def api_get_listModels(
    request: project.listModels_service.GetModelsRequest,
) -> project.listModels_service.GetModelsResponse | Response:
    """
    Retrieves a list of available AI models that users can select for content generation. This endpoint might internally call LiteLLM to fetch supported models like gpt-4-turbo. The response includes an array of models with details such as model name, description, and availability.
    """
    try:
        res = await project.listModels_service.listModels(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/templates", response_model=project.createTemplate_service.CreateTemplateResponse
)
async def api_post_createTemplate(
    title: str, content: str, metadata: Dict[str, str]
) -> project.createTemplate_service.CreateTemplateResponse | Response:
    """
    Creates a new email template. This endpoint accepts JSON-formatted input including template attributes like title, content, and metadata. It would use data validation to ensure required fields are provided before storing. Expected response is the newly created template object with an HTTP 201 status on success.
    """
    try:
        res = await project.createTemplate_service.createTemplate(
            title, content, metadata
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/models/feedback",
    response_model=project.getModelFeedback_service.ModelFeedbackResponse,
)
async def api_get_getModelFeedback(
    model_id: str, date_range: Tuple[date, date], feedback_type: str
) -> project.getModelFeedback_service.ModelFeedbackResponse | Response:
    """
    Fetches feedback from the Quality Check Module regarding the performance of the currently selected AI model. This could include metrics like accuracy, user satisfaction ratings, and error rates. This data aids in assessing model efficacy and guides future selections.
    """
    try:
        res = await project.getModelFeedback_service.getModelFeedback(
            model_id, date_range, feedback_type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/quality-check/validate",
    response_model=project.validateContent_service.ContentValidationResponse,
)
async def api_post_validateContent(
    content: str,
) -> project.validateContent_service.ContentValidationResponse | Response:
    """
    Validates AI-generated content by submitting it to a secondary AI model. Expects a JSON payload with 'content' from the AI Writing Module. Returns validation results including error checks and suggestions.
    """
    try:
        res = await project.validateContent_service.validateContent(content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/drafts", response_model=project.createDraft_service.CreateDraftResponse)
async def api_post_createDraft(
    content: str, modelId: Optional[str], userId: str
) -> project.createDraft_service.CreateDraftResponse | Response:
    """
    Creates a new draft with initial content generated by AI or input manually by users. This endpoint mirrors the capability of AI integrations like gpt-4-turbo to generate initial draft content. Input: {content: string}, Response: {draftId: string, created: boolean}.
    """
    try:
        res = await project.createDraft_service.createDraft(content, modelId, userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/templates", response_model=project.listTemplates_service.GetTemplatesResponse
)
async def api_get_listTemplates(
    page: int, limit: int, category: Optional[str], sortBy: str
) -> project.listTemplates_service.GetTemplatesResponse | Response:
    """
    Retrieves a list of all available email templates. It returns an array of template objects, sorted by most recently updated. This endpoint supports pagination and filtering parameters to handle large volumes of data.
    """
    try:
        res = await project.listTemplates_service.listTemplates(
            page, limit, category, sortBy
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/drafts/{draftId}", response_model=project.updateDraft_service.UpdateDraftResponse
)
async def api_put_updateDraft(
    draftId: str, content: str
) -> project.updateDraft_service.UpdateDraftResponse | Response:
    """
    Updates the content of an existing draft identified by the draftId. It accepts revised content and updates the draft in the database. Used primarily by users in editing roles to refine and finalize drafts. Input expected: {content: string}, Response: {draftId: string, updated: boolean}.
    """
    try:
        res = await project.updateDraft_service.updateDraft(draftId, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/analytics/emails",
    response_model=project.createEmailAnalysis_service.EmailAnalysisResponse,
)
async def api_post_createEmailAnalysis(
    date_from: datetime, date_to: datetime, campaign_id: Optional[str]
) -> project.createEmailAnalysis_service.EmailAnalysisResponse | Response:
    """
    Initiates a detailed analysis of newly sent emails. This endpoint should be called after an email is dispatched through the AI Writing Module. It processes outcomes and stores them for future retrieval and reporting.
    """
    try:
        res = await project.createEmailAnalysis_service.createEmailAnalysis(
            date_from, date_to, campaign_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/ai-writing/content/{contentId}",
    response_model=project.fetchGeneratedContent_service.GetAIContentResponse,
)
async def api_get_fetchGeneratedContent(
    contentId: str,
) -> project.fetchGeneratedContent_service.GetAIContentResponse | Response:
    """
    Retrieves the generated content from a prior request, identified by contentId. It outputs the full content if it's been validated by the Quality Check Module, along with metadata regarding the used model and validation status.
    """
    try:
        res = await project.fetchGeneratedContent_service.fetchGeneratedContent(
            contentId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/ai-writing/content",
    response_model=project.createContentRequest_service.ContentGenerationResponse,
)
async def api_post_createContentRequest(
    userId: str,
    contentParameters: project.createContentRequest_service.ContentParameters,
    modelType: project.createContentRequest_service.ModelType,
) -> project.createContentRequest_service.ContentGenerationResponse | Response:
    """
    Creates a new content generation request using the gpt-4-turbo model, potentially redirected by the Model Selection Module based on availability and suitability. Once content is generated, it's submitted to the Quality Check Module for validation. Expected to return the new content's ID and a status of the creation process.
    """
    try:
        res = await project.createContentRequest_service.createContentRequest(
            userId, contentParameters, modelType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/quality-check/list",
    response_model=project.listValidations_service.ListQualityChecksResponse,
)
async def api_get_listValidations(
    limit: Optional[int], offset: Optional[int]
) -> project.listValidations_service.ListQualityChecksResponse | Response:
    """
    Lists recent content validations submitted to the module. Provides a summary of each validation, including IDs, submission times, and status.
    """
    try:
        res = await project.listValidations_service.listValidations(limit, offset)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/analytics", response_model=project.getAnalytics_service.EmailAnalyticsResponse
)
async def api_get_getAnalytics(
    request: project.getAnalytics_service.GetEmailAnalyticsRequest,
) -> project.getAnalytics_service.EmailAnalyticsResponse | Response:
    """
    Retrieves overall performance statistics of sent emails. It pulls email outcome data from the AI Writing Module to provide key metrics and trends such as open rate, click-through rate, and conversion metrics. This endpoint serves aggregated data suitable for dashboards and reports.
    """
    try:
        res = await project.getAnalytics_service.getAnalytics(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/analytics/emails/{emailId}",
    response_model=project.updateEmailAnalysis_service.EmailAnalyticsUpdatedResponse,
)
async def api_patch_updateEmailAnalysis(
    emailId: str, openRate: Optional[float], conversionRate: Optional[float]
) -> project.updateEmailAnalysis_service.EmailAnalyticsUpdatedResponse | Response:
    """
    Updates existing analytics data for a specific email. This endpoint accommodates changes or recalculations in email performance metrics and can be used to correct or enhance analytics accuracy.
    """
    try:
        res = await project.updateEmailAnalysis_service.updateEmailAnalysis(
            emailId, openRate, conversionRate
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/quality-check/status/{validationId}",
    response_model=project.getValidationStatus_service.QualityCheckStatusResponse,
)
async def api_get_getValidationStatus(
    validationId: str,
) -> project.getValidationStatus_service.QualityCheckStatusResponse | Response:
    """
    Retrieves the status of a content validation process. The {validationId} is a unique identifier for a validation request. It returns the current status and any results if available.
    """
    try:
        res = await project.getValidationStatus_service.getValidationStatus(
            validationId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/models/select", response_model=project.selectModel_service.ModelSelectionResponse
)
async def api_post_selectModel(
    modelIdentifier: project.selectModel_service.ModelType,
) -> project.selectModel_service.ModelSelectionResponse | Response:
    """
    Allows a user to select a specific AI model for their session of content generation. Sends the chosen model name (e.g., gpt-4-turbo) to the AI Writing Module and stores this preference for future use. The request should include the model identifier. The expected response would confirm the successful selection, including the model name and status.
    """
    try:
        res = await project.selectModel_service.selectModel(modelIdentifier)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/quality-check/update/{validationId}",
    response_model=project.updateValidation_service.QualityCheckUpdateResponse,
)
async def api_put_updateValidation(
    validationId: str,
    newContent: str,
    newModelType: Optional[str],
    additionalNotes: Optional[str],
) -> project.updateValidation_service.QualityCheckUpdateResponse | Response:
    """
    Updates the details or parameters of an existing validation request. Useful for adding notes or adjusting the validation parameters after the initial request.
    """
    try:
        res = await project.updateValidation_service.updateValidation(
            validationId, newContent, newModelType, additionalNotes
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
