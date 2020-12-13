from app import app
from flask import render_template
from data_prep import get_figures
import json, plotly

@app.route('/')
def index():
  figures = get_figures()

  figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('main.html', figuresJSON=figuresJSON)