from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from starlette.responses import FileResponse
app = FastAPI()
@app.get("/images/{image_id}")
def get_image(image_id):
    return FileResponse("./images/" + image_id)
    #return Response(image_id,mimetype="text/event-stream")
