# blog-engine



### TODO
1. finish the instruction
2. create another sub app to post the technical post
3. reorganize the infrastructure of the blog engine(life-blog and technical-blog)


### start your own django project
After you install django, type in:
`django-admin startproject <myblog>`

### database setting
By default, django use sqlite. But just in case the project get larger, I use mysql here.

### create a virtual python environment
`cd <myblog>`
`virtualenv -p /usr/bin/python3 env`
`source env/bin/activate`

### install python required package
`pip install -r requirements.txt`

### create a new sub app
`python manage.py startapp <blog-name>`
`python manage.py makemigrations <blog-name>`

### after you created all the sub app that you need
`python manage,py migrate`

### create admin user
`python manage.py createsuperuser`

Then clone this repo and run command `cp blog/* <your-blog-name>`  
Open the <blog>/settings.py and in the row *INSTALLED_APPS* append '<blog-name>', 'markdown_deux' into the dictionary.





### Voila
