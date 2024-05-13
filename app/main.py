from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse, HTMLResponse, RedirectResponse
from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.staticfiles import StaticFiles

from json import loads, dumps
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import json
import pprint

matplotlib.use('WebAgg')
plt.style.use('ggplot')

tags_metadata = [

    {
        "name": "Attribute",
        "description": "Display unique count data from Pandas DataFrame for column 'Attribute'",
    },
    {
        "name": "Commodity",
        "description": "Display unique count data from Pandas DataFrame for column 'Commodity'",
    },
    {
        "name": "CommodityType",
        "description": "Display unique count data from Pandas DataFrame for column 'CommodityType'",
    },
    {
        "name": "Units",
        "description": "Display unique count data from Pandas DataFrame for column 'Units'",
    },
    {
        "name": "YearType",
        "description": "Display unique count data from Pandas DataFrame for column 'YearType'",
    },
    {
        "name": "Year",
        "description": "Display unique count data from Pandas DataFrame for column 'Year'",
    },
    {
        "name": "Value",
        "description": "Display unique count data from Pandas DataFrame for column 'Value'",
    },

]
app = FastAPI(openapi_tags=tags_metadata)
app.mount("/static", StaticFiles(directory="/code/app/static"), name="static")

# Try to read in file, if not, all other pages will be redirected for to a NotFound page
fileFound = True
try:
    projectionFile = pd.read_csv('/code/app/static/Projection2021.csv')
except:
    fileFound = False

def plot(column_name):
    fig, ax = plt.subplots(figsize=(100, 50))
    hist = projectionFile[column_name].value_counts()
    hist.name = column_name
    x = hist.index
    y = hist.values
    plt.yticks(fontsize=35)
    plt.xticks(fontsize=35)

    ax.barh(x, y)
    fig.canvas.draw()
    png_output = io.BytesIO()
    FigureCanvas(fig).print_png(png_output)
    pngFile = f'static/{column_name}.png'
    fig.savefig(pngFile)
    return Response(content=png_output.getvalue(), media_type='image/png')

@app.get("/")
def MainPage():
    if fileFound:
        return RedirectResponse("http://127.0.0.1:8000/docs")
    else:
        html_not_found = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>No File Found</title>
            </head>
            <body>
                <h1>No File '{}' Found</h1>
                Please make sure a valid CSV file named: <b> Projection2021.csv </b> is inside the /app folder.
            </body>
        </html>""".format('Projection2021.csv')
        return HTMLResponse(content=html_not_found, status_code=404)


@app.get("/Attribute/histogram")
async def AttributeHist(return_plot: bool = False, tags=['Attribute']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("Attribute")
    else:
        return HTMLResponse(content=projectionFile['Attribute'].value_counts().to_frame().to_html(), status_code=200)

@app.get("/Commodity/histogram")
async def CommodityHist(return_plot: bool = False, tags=['Commodity']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("Commodity")
    else:
        return HTMLResponse(content=projectionFile['Commodity'].value_counts().to_frame().to_html(), status_code=200)

@app.get("/CommodityType/histogram")
async def CommodityTypeHist(return_plot: bool = False, tags=['CommodityType']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("CommodityType")
    else:
        return HTMLResponse(content=projectionFile['CommodityType'].value_counts().to_frame().to_html(), status_code=200)

@app.get("/Units/histogram")
async def UnitsHist(return_plot: bool = False, tags=['Units']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("Units")
    else:
        return HTMLResponse(content=projectionFile['Units'].value_counts().to_frame().to_html(), status_code=200)

@app.get("/YearType/histogram")
async def YearTypeHist(return_plot: bool = False, tags=['YearType']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("YearType")
    else:
        return HTMLResponse(content=projectionFile['YearType'].value_counts().to_frame().to_html(), status_code=200)

@app.get("/Year/histogram")
async def YearHist(return_plot: bool = False, tags=['YearHist']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("Year")
    else:
        return HTMLResponse(content=projectionFile['Year'].value_counts().to_frame().to_html(), status_code=200)


@app.get("/Value/histogram")
async def ValueHist(return_plot: bool = False, tags=['Value']):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1:8000/")
    elif return_plot:
        return plot("Value")
    else:
        return HTMLResponse(content=projectionFile['Value'].value_counts().to_frame().to_html(), status_code=200)
