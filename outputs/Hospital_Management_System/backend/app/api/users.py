from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .services.user_service import UserService
from .schemas.user import UserSchema

app = FastAPI()

user_service = UserService("sqlite:///users.db")

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = user_service.get_user(user_id)
    if user:
        return JSONResponse(content={"id": user.id, "username": user.username, "role": user.role}, media_type="application/json")
    return JSONResponse(content={"error": "User not found"}, media_type="application/json", status_code=404)

@app.post("/users/")
async def create_user(user: UserSchema):
    new_user = user_service.create_user(user.dict())
    return JSONResponse(content={"id": new_user.id, "username": new_user.username, "role": new_user.role}, media_type="application/json")

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserSchema):
    updated_user = user_service.update_user(user_id, user.dict())
    if updated_user:
        return JSONResponse(content={"id": updated_user.id, "username": updated_user.username, "role": updated_user.role}, media_type="application/json")
    return JSONResponse(content={"error": "User not found"}, media_type="application/json", status_code=404)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    deleted = user_service.delete_user(user_id)
    if deleted:
        return JSONResponse(content={"message": "User deleted successfully"}, media_type="application/json")
    return JSONResponse(content={"error": "User not found"}, media_type="application/json", status_code=404)