from fastapi import APIRouter, Depends
import os
from fastapi import HTTPException
from redis.exceptions import RedisError
from utils import MyRepository
from redis_client import r
from routers.auth import get_current_user

router = APIRouter()

@router.get('/repository/info')
async def get_repository_info(current_user = Depends(get_current_user)):
    repo_name = os.getenv("SVN_REPO_NAME")
    if not repo_name:
        raise HTTPException(status_code=500, detail={
            'error_code': 'REPOSITORY_INFO_ERROR',
            'message': "Error! Can't get the name of the repository!"
        })
    return {'name': repo_name}

@router.get("/repository/content")
async def get_repository_content(path: str, current_user = Depends(get_current_user)):
    repository_url = "file:///local_svn"
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return MyRepository.getPcbContent(repository_url, path)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                'error_code': 'REPOSITORY_CONTENT_ERROR',
                'message': str(e)
            })
    else:
        try:
            return MyRepository.getFolderList(repository_url, path)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                'error_code': 'REPOSITORY_CONTENT_ERROR',
                'message': str(e)
            })

@router.get("/repository/statistics")
async def get_repository_statistics(current_user = Depends(get_current_user)):
    try:
        schlib_count = int(r.get('schlib_count') or 0)
        pcblib_count = int(r.get('pcblib_count') or 0)
        footprints_count = int(r.get('footprints_count') or 0)
        symbols_count = int(r.get('symbols_count') or 0)
        return {
            "schlib_count": schlib_count,
            "pcblib_count": pcblib_count,
            "footprints_count": footprints_count,
            "symbols_count": symbols_count,
        }
    except RedisError as e:
        raise HTTPException(status_code=503, detail={
            'error_code': 'REPOSITORY_STATISTICS_ERROR',
            'message': str(e)
        })