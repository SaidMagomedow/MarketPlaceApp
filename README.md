Market Place 

The project is at the stage of refactoring, optimization and writing new features.


Required Components: To run, you need to install the following components:

docker (version 18.06 or higher) docker-compose (version 1.22 or higher) To start the project, you need to run the following commands:

1. Clone the repository from git - git clone https://github.com/SaidMagomedow/05ruShop.git
2. Build docker image - docker-compose build
3. Up docker container - docker-compose up
4. Build migrations - docker-compose run --rm web python manage.py migrate