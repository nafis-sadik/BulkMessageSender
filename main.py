import os
import uvicorn
from dotenv import find_dotenv, load_dotenv

from WebApplication import app

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app=app, host='0.0.0.0', port=port)
