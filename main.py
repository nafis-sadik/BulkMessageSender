import os
import uvicorn

from WebApplication import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app=app, host='0.0.0.0', port=port)
