## Power Rankings Backend

Keeps data via SQLModel and SQLite on power rankings for the frolf coalition

### Prerequisites
- Python 3.11 or 3.12 recommended
- Install `uv` (fast Python package manager)
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `irm https://astral.sh/uv/install.ps1 | iex`

### 1) Create a virtual environment
```bash
uv venv
```

Activate it:
- macOS/Linux:
```bash
source .venv/bin/activate
```
- Windows (PowerShell):
```powershell
.venv\\Scripts\\Activate.ps1
```

### 2) Install dependencies
```bash
uv pip install -r requirements.txt
```

### 3) Configuration
Copy the example environment file and adjust as needed:
```bash
cp env.example .env
```

Environment variables:
- `DATABASE_URL`: SQLAlchemy URL for the database. Defaults to `sqlite:///./app.db`.

SQLite files will be created in the project root by default.

### 4) Run the development server
Using uv to run Uvicorn with auto-reload:
```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000/docs` for interactive API docs.

### Project structure
```text
app/
  __init__.py
  main.py            # FastAPI app/entrypoint
  config.py          # App settings from env
  db.py              # Engine/session creation and table init
  models.py          # SQLModel models
  api/
    __init__.py
    routes.py        # API routers and endpoints
env.example          # Example environment config
requirements.txt     # Dependencies for uv pip
README.md            # This file
```

### Common tasks
- Run with a different DB URL:
```bash
DATABASE_URL="sqlite:///./dev.db" uv run uvicorn app.main:app --reload
```

- Reset SQLite DB (dangerous: deletes file):
```bash
rm -f app.db
```

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Free Tier)
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Deploy** - Railway will auto-detect Python and use `railway.toml`
4. **Get URL** - Your API will be live at `https://your-app-name.railway.app`

### Option 2: Render (Free Tier)
1. **Sign up** at [render.com](https://render.com)
2. **New Web Service** → Connect GitHub repo
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Deploy** - Your API will be live at `https://your-app-name.onrender.com`

### Option 3: Heroku (Paid)
1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: `git push heroku main`
5. **Open**: `heroku open`

### Option 4: DigitalOcean App Platform
1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create App** → Connect GitHub
3. **Configure**:
   - Source: GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Deploy** - Get your live URL

### Option 5: Docker Deployment
```bash
# Build image
docker build -t power-rankings-backend .

# Run container
docker run -p 8000:8000 power-rankings-backend

# Or use docker-compose
docker-compose up -d
```

### Option 6: VPS Deployment (Ubuntu/Debian)
```bash
# On your VPS
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone repo
git clone https://github.com/yourusername/power-rankings-backend.git
cd power-rankings-backend

# Install dependencies
pip3 install -r requirements.txt

# Install systemd service
sudo nano /etc/systemd/system/power-rankings.service
```

**Systemd service file** (`/etc/systemd/system/power-rankings.service`):
```ini
[Unit]
Description=Power Rankings Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/power-rankings-backend
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable power-rankings
sudo systemctl start power-rankings

# Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/power-rankings
```

**Nginx config** (`/etc/nginx/sites-available/power-rankings`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site and restart nginx
sudo ln -s /etc/nginx/sites-available/power-rankings /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 Production Considerations

### Environment Variables
- Set `DATABASE_URL` for production database
- Set `ENVIRONMENT=production`
- Consider using PostgreSQL for production

### Security
- Add CORS middleware for frontend integration
- Implement authentication if needed
- Use HTTPS in production
- Set up proper logging

### Monitoring
- Add health check endpoint (`/api/health`)
- Set up error tracking (Sentry)
- Monitor performance metrics

## 🌐 Custom Domain Setup (GoDaddy)

### Quick Setup Steps:
1. **Deploy** your app to Railway/Render/DigitalOcean
2. **Get deployment URL** (e.g., `https://power-rankings-backend-production.railway.app`)
3. **Add custom domain** in your hosting platform
4. **Configure DNS** in GoDaddy:
   - Go to DNS Management
   - Add CNAME record: `api` → `your-deployment-url.com`
5. **Wait for propagation** (5-60 minutes)
6. **Test**: `https://api.yourdomain.com/api/health`

### Example:
- **Domain**: `frolfapi.com`
- **API URL**: `https://api.frolfapi.com`
- **Test**: `curl https://api.frolfapi.com/api/players`

📖 **Detailed instructions**: See `DOMAIN_SETUP.md` for complete guide.