from app import app
from waitress import serve

serve(
    app.server,
    port=8030
)