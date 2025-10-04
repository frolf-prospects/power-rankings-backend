# Domain Configuration Guide

## 🌐 Connecting GoDaddy Domain to Your Backend

### Step 1: Choose Your Hosting Platform

**Recommended platforms that support custom domains:**
- **Railway** (Free tier supports custom domains)
- **Render** (Free tier supports custom domains) 
- **DigitalOcean App Platform** (Paid, but reliable)
- **Heroku** (Paid, but easy setup)

### Step 2: Get Your Deployment URL

After deploying to your chosen platform, you'll get a URL like:
- Railway: `https://power-rankings-backend-production.railway.app`
- Render: `https://power-rankings-backend.onrender.com`
- DigitalOcean: `https://power-rankings-backend-xyz.ondigitalocean.app`

### Step 3: Configure Custom Domain in Hosting Platform

#### For Railway:
1. Go to your project dashboard
2. Click on your service
3. Go to "Settings" → "Domains"
4. Click "Add Domain"
5. Enter your domain (e.g., `api.yourdomain.com`)
6. Railway will provide DNS records to configure

#### For Render:
1. Go to your service dashboard
2. Click "Settings" → "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain
5. Render will provide DNS configuration

#### For DigitalOcean:
1. Go to your app dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Get DNS configuration instructions

### Step 4: Configure DNS in GoDaddy

1. **Log into GoDaddy** account
2. **Go to DNS Management**:
   - Go to "My Products" → "Domains"
   - Click "Manage" next to your domain
   - Click "DNS" tab

3. **Add/Update DNS Records**:

#### Option A: Subdomain (Recommended)
Add a CNAME record:
```
Type: CNAME
Name: api (or whatever subdomain you want)
Value: your-deployment-url.com
TTL: 600 (or default)
```

**Example:**
- Domain: `yourdomain.com`
- Subdomain: `api.yourdomain.com`
- Points to: `power-rankings-backend-production.railway.app`

#### Option B: Root Domain
Add an A record:
```
Type: A
Name: @
Value: [IP address from hosting platform]
TTL: 600
```

**Note:** Most platforms provide IP addresses for A records.

### Step 5: SSL Certificate Setup

Most platforms automatically handle SSL certificates for custom domains:
- **Railway**: Automatic SSL
- **Render**: Automatic SSL
- **DigitalOcean**: Automatic SSL

### Step 6: Test Your Domain

After DNS propagation (5-60 minutes):
```bash
# Test your custom domain
curl https://api.yourdomain.com/api/health

# Should return: {"status": "ok"}
```

### Common DNS Record Types:

#### CNAME Record (Recommended for subdomains):
```
Type: CNAME
Name: api
Value: power-rankings-backend-production.railway.app
```

#### A Record (For root domain):
```
Type: A
Name: @
Value: 192.168.1.1 (example IP)
```

#### AAAA Record (IPv6):
```
Type: AAAA
Name: @
Value: 2001:db8::1 (example IPv6)
```

### Troubleshooting:

1. **DNS Propagation**: Can take up to 48 hours (usually 5-60 minutes)
2. **Check DNS**: Use `nslookup api.yourdomain.com` or online DNS checker
3. **SSL Issues**: Wait for automatic SSL certificate generation
4. **Caching**: Clear browser cache or use incognito mode

### Example Complete Setup:

**Domain**: `frolfapi.com`
**Subdomain**: `api.frolfapi.com`
**Points to**: `power-rankings-backend-production.railway.app`

**GoDaddy DNS Configuration:**
```
Type: CNAME
Name: api
Value: power-rankings-backend-production.railway.app
TTL: 600
```

**Result**: `https://api.frolfapi.com/api/players` will serve your API!
