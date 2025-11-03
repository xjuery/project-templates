# FastAPI Backend

FastAPI backend for OAuth2/OIDC integration.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the script
./run.sh
```

## API Endpoints

- `GET /` - API root
- `GET /api/public/info` - Public endpoint
- `GET /api/user/profile` - Protected endpoint (requires Bearer token)

## Configuration

Edit `app/main.py` to configure:
- OIDC Issuer URL
- CORS origins
- Client ID

