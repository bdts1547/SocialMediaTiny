# SocialMediaTiny

## Installation
**Docker**: require docker compose
```
git clone https://github.com/bdts1547/SocialMediaTiny.git
docker-compose build
docker-compose up
```
then go to: [localhost:8000](http://localhost:8000)

**Window/Linux**: required python3.9
```
git clone https://github.com/bdts1547/SocialMediaTiny.git
pip install -r requirements.txt
python manage.py runserver
```

SuperUserAccount: 
- Username: dangnh
- Password: 123

## Description
***A simple social network with features like:***

- Authentication & Authorization: Login/Logout, Email OTP reset password, User & Group Management
- CRUD methods: upload, edit, delete post, image, comments, like, follow
- Pagination, Search
- Ban/Unban User

***Technologies***:
 Python-Django, AJAX, Javascript-DOM, SQLite, Firebase Storage.



## Todo List
- [x] Register, Login, Logout
- [x] Profile, Setting
- [x] Upload and Get URL image from Firebase Storage
- [x] Upload, Edit, Delete post
- [x] Comment, Like, Follow
- [x] Ban & Unban User
- [x] Pagination, Search
- [x] OAuth with Google
- [x] Submit without refresh page with AJAX
- [x] Authentication & Authorization (Login/Logout, Email OTP reset password, User & Group Management)
- [ ] Notification
- [ ] Chat-realtime
- [ ] PageGroup
- [ ] Edit comment





