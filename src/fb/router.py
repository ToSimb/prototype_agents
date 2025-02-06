from fastapi import APIRouter, HTTPException, Depends, Request

router = APIRouter(
    prefix="/fb",
    tags=["F_B"]
)
def get_db_pool(request: Request):
    return request.app.state.db_connection

@router.get("/{name_int}")
async def get_data_fa(name_int: int, db_connection=Depends(get_db_pool)):
    try:
        print(name_int)
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM fb WHERE id = ?", (name_int,))
        result = cursor.fetchall()
        print(result[0][1])
        cursor.close()
        if not result:
            raise HTTPException(status_code=404, detail="Данные не найдены.")
        return result[0][1]
    except FileNotFoundError:
        return ("нет такого узла")
    except Exception as e:
        error_str = f"Exception: {e}."
        raise HTTPException(status_code=527, detail={"error_msg": error_str})