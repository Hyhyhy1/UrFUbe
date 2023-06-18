from typing import List
import boto3

from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from starlette.requests import Request, Message
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from user.auth import current_active_user

from video.schemas import GetListVideo
from video.models import Video, User
from video.services import save_video#, open_file

video_router = APIRouter()
templates = Jinja2Templates(directory="templates")
s3 = boto3.client("s3",
                endpoint_url='',
                aws_access_key_id='',
                aws_secret_access_key='')


@video_router.post("/videos/upload")
async def upload_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        user: User = Depends(current_active_user)):
    return await save_video(user, file, title, description, background_tasks)


@video_router.get("/video/{video_pk}", response_model=Video, responses={404: {"model": Message}})
async def get_video(video_pk: int):
    file = await Video.objects.select_related('user').get(pk=video_pk)

    try:
        result = s3.get_object(Bucket="UrFUbe-videos", Key=file.dict().get('file'))
        return StreamingResponse(content=result["Body"].iter_chunks(), media_type=file.dict().get('file_type'))
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))


@video_router.get("/user/{username}", response_model=List[GetListVideo])
async def get_video_list(username: str):
    user = await User.objects.get(username=username)
    print(user)
    user_pk = user.dict().get('id')
    print(user_pk)
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    file = await Video.objects.get(pk=video_pk)
    video_type = file.dict().get('file_type')
    return templates.TemplateResponse("index.html", {"request": request, "path": video_pk, "type": video_type})


@video_router.get("/videos/upload", response_class=HTMLResponse)
async def get_video(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})


'''
@video_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)

    video = await Video.objects.get(pk=video_pk)
    video_type = video.dict().get('file_type')
    response = StreamingResponse(file, media_type=video_type, status_code=status_code,)

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response
'''