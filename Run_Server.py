import uvicorn

if __name__ == '__main__':
    uvicorn. run('API.Save_Data_API:app', host='0.0.0.0', port=666, reload=True)
