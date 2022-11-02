# Quick_transfer

This is a Banking API I created as a part of a technical interview.

## Features
<li> Create new account and get a verification email.
<li> Transfer  money from one account to another.
<li> Consult transfers history
<li> Consult Profile
<li> Consult all users



## Prerequisites
1. A Terminal (preferred) or a CMD
2. Python 3
3. Django
4. django-environ
5. djangorestframework
6. djangorestframework-simplejwt

more details about version in the requirements.txt file

## Installation
1. Open a Terminal, and clone the current repository.
    ```
    git clone https://github.com/moez552/quick_transfer.git
    ```
2. Enter the root directory.
    ```
    cd quick_transfer
    ```

3. Now start the setup by entering the following command.
    ```
    python manage.py runserver
    ```
    If that didn't work, try replacing `python` by `python3` in the above command.
    
   you may incounter migrations errors I suggest you run:
       ```
     python manage.py makemigrations
     python manage.py migrate
       ```
  

### endpoints: 
<li> /register : register a new user
<li> /api/token : get authentication token
<li> /api/token/refresh/ : refresh token
<li> /profile : your profile
<li> /users ; list of users
<li> /history : your transactions history
