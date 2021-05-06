# Kira 
Kira is an app builded in Django Framework. It is an assisstant that helps to create Database query-table from an Excel file. In one section is showed the AVRO Schema of the Excel file.

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/guido-lab/kira.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Apply the migrations:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.


## License

The source code is released for Kira
