from app import FinancesService

application = FinancesService().wsgi_app

if __name__ == "__main__":
    application.run()