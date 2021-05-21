from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fasteda import *
import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory="template")



def process_data(request: Request):
    try:
        fasteda = FastEda(filedetail)
        process = fasteda.process
        return templates.TemplateResponse('FastEda.html', 
                context={'request': request, 'title': 'Workspace', 
                        'fname': filedetail.filename,\
                        'sample': fasteda.file_columns(),\
                        'quick': fasteda.quick_stat(),\
                        'corr': fasteda.correlation(),\
                        'process': process})

    except Exception as e:
        
        return templates.TemplateResponse('error_file.html', context={'request': request, 'error': str(e)})


@app.get('/')
async def home(requset: Request):
    return process_data(requset)


def start(filename: str, dm=','):
    try:
        df = pd.read_csv(filename, delimiter=dm)

        global filedetail
        filedetail = FileDetail(filename = filename[15:], 
                            filetype = filename.split('.')[-1], 
                            filesize=f"{os.stat(filename).st_size} bytes", 
                            sysfilepath=filename, 
                            obj=df,
                            missing = df.isna().sum().values.sum(),
                            objcopy = df.copy())

        
        uvicorn.run(app)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    path = 'static/dataset/cars.csv'
    start(path)