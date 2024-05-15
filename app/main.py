import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io
import json
import pprint
import numpy as np

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse, HTMLResponse, RedirectResponse
from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from json import loads, dumps
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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
    pngFile = f'/code/app/static/{column_name}.png'
    fig.savefig(pngFile)
    return Response(content=png_output.getvalue(), media_type='image/png')

def response(column_name, return_plot):
    if not fileFound:
        return RedirectResponse("http://127.0.0.1/docs")
    elif return_plot:
        return plot(column_name)
    else:
        return HTMLResponse(content=projectionFile[column_name].value_counts().to_frame().to_html(), status_code=200)

@app.get("/")
def MainPage():
    if not fileFound:
        return RedirectResponse("http://127.0.0.1/docs")
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
async def AttributeHist(return_plot: bool = False):
    return response("Attribute", return_plot)

@app.get("/Commodity/histogram", tags=['Commodity'])
async def CommodityHist(return_plot: bool = False):
    return response("Commodity", return_plot)

@app.get("/CommodityType/histogram", tags=['CommodityType'])
async def CommodityTypeHist(return_plot: bool = False):
    return response("Commodity", return_plot)

@app.get("/Units/histogram", tags=['Units'])
async def UnitsHist(return_plot: bool = False):
    return response("CommodityType", return_plot)

@app.get("/YearType/histogram", tags=['YearType'])
async def YearTypeHist(return_plot: bool = False):
    return response("YearType", return_plot)

@app.get("/Year/histogram", tags=['YearHist'])
async def YearHist(return_plot: bool = False):
    return response("Year", return_plot)

@app.get("/Value/histogram", tags=['Value'])
async def ValueHist(return_plot: bool = False):
    return response("Value", return_plot)
