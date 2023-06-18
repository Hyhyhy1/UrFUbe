import boto3
from uuid import uuid4
from fastapi import UploadFile, HTTPException, BackgroundTasks

from video.schemas import UploadVideo
from video.models import Video, User

s3 = boto3.client('s3',
                    endpoint_url='',
                    aws_access_key_id='',
                    aws_secret_access_key='')

'''
def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()
'''





async def save_video(user: User,
                     file: UploadFile,
                     title: str,
                     description: str,
                     background_tasks: BackgroundTasks):

    file_name = f'{user.id}/{uuid4()}.{file.filename.split(".")[-1]}'

    if file.content_type == 'video/quicktime' \
            or file.content_type == 'video/x-ms-wmv' or file.content_type == 'video/x-matroska':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail='Wrong video format')

    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, file_type=file.content_type, user=user.dict(), **info.dict())


def write_video(filename: str, file: UploadFile):
    try:
        bucket_name = 'UrFUbe-videos'
        s3.upload_fileobj(file.file, bucket_name, filename, ExtraArgs={"ACL": "public-read"})
    except Exception:
        raise HTTPException(status_code=500, detail='Video upload went wrong')

'''
async def open_file(request: Request, video_pk: int) -> tuple:
    try:
        video_data = await Video.objects.get(pk=video_pk)
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404, detail='Not found')

    path = video_data.dict().get('file')
    file = s3.get_object(Bucket="UrFUbe-videos", Key=path)
    file_size = file['ContentLength']

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers
'''