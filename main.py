from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI()

hotels = [{"id": 1, "title": "Sochi", "name": "sochi"},
          {"id": 2, "title": "Dubai", "name": "dubai"}]


@app.get("/hotels")
def hotel_get(
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete("/hotels/{hotel_id}")
def hotel_delete(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def hotel_post(title: str = Body(embed=True)):
    global hotels
    hotel_id = len(hotels) + 1
    hotels.append({
        "id": hotel_id,
        "title": title}

    )
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
