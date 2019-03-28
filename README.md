# Placeholder

Placeholder is a FOSS, Django based project to generate image placeholders on the fly with a range of size, color, format and text options. This project is running live at https://placeholder.amid.africa.

### Installing

You will need to have Python 3.5+ on your system. You will need to set up a virtual environment. Instruction on how to install Python and setup a virtual environment vary between OS’s. There are vast resources available and it would not be good to try to put them all here. Rather try to search on google for the instructions for your OS.

Download and extract the project into a folder of your choice. With your virtual environment activated, install the requirements:

```
pip install -r requirements.txt
```

As the project does not use any models, you do not need to perform migrations. To run the project in your local environment, use the command:

```
python manage.py runserver 8000
```

### Running

Placeholders are generated in the following format:
```
http://127.0.0.1:8000/width/height/backcolor/forecolor/format/?text=custom
```
* Only the width is required, all others are optional. However, if you want to set the forecolor, you have to also set the backcolor.

* The width and height are in pixels. 

* The backcolor and forecolour are 6 character hex values, with NO preceding hash character.

* The default format is PNG. Other options are BMP, GIF, JPG and PCX.

* Lastly, you may customise the second line of text on the placeholder.


## What is Amid Africa.

Amid Africa is a movement to encourage developers in Africa to use the Python language and in particular the Django framework. You can find out more about Amid Africa the projects we are working on or joining us at https://amid.africa
