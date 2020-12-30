## Disaster Response Pipeline

### About The Project

After disaster happen a lot of people suffered from the tragedy. To save every living survivor, we need give them the best response we can give. But, it is difficult to know what actually the survivor need fast. This project will help the volunteer to tackle this problem.

In this project, I try to create a model to predict what actually survivor need based on given text and categorize them into 36 categories. This will help volunteers to prepare and give what the survivor really needs.

### Getting Started

to test the code, use the following commands:

- **ETL Pipeline**
from root folder: `python3 datasets/process_data.py datasets/messages.csv datasets/categories.csv datasets/DisasterResponse.db`

- **ML Pipeline**
from root folder move to `cd web-app/app`, then
`python3 train_classifier.py database/DisasterResponse.db models/model.pickle test`.
the last `test` argument used if only you need quick train with 100 rows only, if you want to train with full dataset, just change `test` to any other string

- **Web Depoylment**
from root folder move to `cd web-app/app`, then
`flask run`

### Folder Structure

#### datasets/

- **messages.csv**
raw file that contains all the messages used for training and testing
- **categories.csv**
raw file that contain all the category for each message in messages.csv
- **DisasterResponse.db**
sqlite database used to store cleaned data
- **datasets/process_data.py**
codes for ETL Pipeline based on ETL_Pipeline.ipynb file
to run this file use `python3 datasets/process_data.py datasets/messages.csv datasets/categories.csv datasets/DisasterResponse.db` from root folder

#### notebooks/

- **ETL_pipeline.ipynb**
Jupyter notebook file that contain ETL pipeline prototyping
- **ML_Pipeline.ipynb**
Jupyter notebook file that contain ML pipeline prototyping

#### web-app/

- **app/train_classfier.py**
codes for ML Pipeline based on ML_Pipeline.ipynb file
to run this file use `python3 train_classifier.py database/DisasterResponse.db models/model.pickle test`. "test" argument used for testing with only 100 rows
- **tokenizer.py**
contain tokenize function so the model can be loaded to `run.py` file
- **app/models/model.pickle**
pickle file to load trained model

### Built With

- [Bootstrap](https://getbootstrap.com)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [Sklearn](https://scikit-learn.org/)

### License

Distributed under the MIT License. See `LICENSE` for more information.

### Contact

Fahmi Abdulaziz - [@fahmiduldul](https://twitter.com/fahmiduldul) - afahmi13@live.com