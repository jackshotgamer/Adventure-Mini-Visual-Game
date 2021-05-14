import uvicorn


def start_server():
    uvicorn.run('API.Save_Data_API:app', host='0.0.0.0', port=666, reload=True)


if __name__ == '__main__':
    start_server()
