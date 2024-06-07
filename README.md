# Instructor Evaluation System For HILCoE

## HOW TO RUN THIS PROJECT
- Install Python(3.11.1) (Dont Forget to Tick Add to Path while installing Python)
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :


```
# to insatll requirments 
pip install -r requirements.txt 
```


```

# to make migrations 
python manage.py makemigrations
python manage.py migrate
```
```
# to create a super user
python manage.py createsuperuser
```
```
change the static configuration to develpment by commenting the production configuration and uncommenting the development
which can be done in the settings.py
```

```
# to run the project
python manage.py runserver
```
```
- Now enter following URL in Your Browser Installed On Your Pc

http://127.0.0.1:8000/

```


  
