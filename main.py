from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/status")
def get_status():
    return {
        "status": "online",
        "version": "0.1.0",
        "day": 1
    }


@app.get("/status")
def get_status():
    return {
        "status": "online",
        "version": "0.1.0",
        "day": 1
    }



@app.get("/about")
def get_about():
    return {
        "project": "My First API",
        "author": "Diana",  
        "course": "Applied Programming"
    }


@app.get("/square/{number}")
def calculate_square(number: int):
    result = number * number
    return {
        "number": number,
        "square": result,
        "calculation": f"{number} x {number} = {result}"
    }


@app.get("/student")
def get_student():
    return {
        "name": "Diana",
        "semester": 1,
        "course": "Wirtschaftsinformatik",
        "university": "Hochschule Coburg"
    }


@app.get("/double/{number}")
def calculate_double(number: int):
    result = number * 2
    return {
        "number": number,
        "double": result,
        "calculation": f"{number} * 2 = {result}"
    }
