from dotenv import load_dotenv
from w18_gabbyevalin import create_app

# lokasi alamat berkas .env
load_dotenv('.env')

app = create_app()

if __name__ == "__main__":
    app.run()
