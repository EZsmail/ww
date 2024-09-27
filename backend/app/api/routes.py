from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from app.database import VideoStateRepository, VideoDataRepository
from app.database.mongo import MongoDBClient
from app.config import DATABASE_URL, UPLOAD_PATH
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

router = APIRouter()

# DB init
db_client = MongoDBClient(uri=DATABASE_URL, db_name="video_db")
video_state_repo = VideoStateRepository(db_client)
video_data_repo = VideoDataRepository(db_client)


@router.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # Проверка подключения к БД
    try:
        client = MongoClient(DATABASE_URL)
        client.admin.command('ping')
        print("MongoDB доступен")
    except ConnectionFailure as e:
        print(f"Ошибка подключения к MongoDB: {e}")

    vid = str(uuid4())
    file_location = f"{UPLOAD_PATH}/{file.filename}"
    
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Добавление состояния видео (начальное состояние "processing")
    video_state_repo.add_video_state(vid, "processing")
    
    # TODO: Отправить задачу в Celery
    # process_video.delay(file_location, vid)
    
    return {"message": "Видео успешно загружено, началась обработка.", "vid": vid}



#get result by id
@router.get("/results/{vid}")
async def get_results(vid: str):
    try:
        result = video_data_repo.get_video_data(vid)
        return {"status": "completed", "data": result["csv"]}
    except ValueError:
        raise HTTPException(status_code=404, detail="Результаты обработки не найдены.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {str(e)}")


#get video status
@router.get("/video-status/{vid}")
async def get_video_status(vid: str):
    try:
        video_state = video_state_repo.get_video_state(vid)
        return {
            "video_id": vid,
            "status": video_state["state"]
        }
    except ValueError:
        raise HTTPException(status_code=404, detail="Видео не найдено.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статуса видео: {str(e)}")
