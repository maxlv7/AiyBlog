from AiyBlog import create_app

manage = create_app("development")

if __name__ == '__main__':
    manage.run()