# Deployment Scripts

## 1. Backend Deployment to Railway

### Prerequisites:
- Railway account at https://railway.app
- GitHub account

### Web Interface Method (Recommended):

1. **Fork this repository** to your GitHub account if you haven't already

2. **Go to Railway.app** and sign in with your GitHub account

3. **Click "New Project"** and select "Deploy from GitHub repo"

4. **Select your forked repository**

5. **Configure the deployment**:
   - **Working Directory**: Set to `/backend`
   - **Builder**: Should automatically detect NIXPACKS due to the Dockerfile
   - **Build Command** (if prompted): `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

6. **Set environment variables** in the Railway dashboard:
   - `OPENAI_API_KEY`: Your OpenRouter API key
   - `OPENAI_BASE_URL`: `https://openrouter.ai/api/v1`
   - `QDRANT_URL`: Your Qdrant database URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `QDRANT_COLLECTION`: Collection name (e.g., `project_documents`)
   - `NEON_DB_URL`: Your Neon database connection string
   - `SECRET_KEY`: A random secret key for JWT
   - `DEBUG`: `false` for production
   - `LOG_LEVEL`: `info`

7. **Deploy** the project

### Railway CLI Method (Alternative):
If you prefer using the CLI:

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Navigate to backend directory**:
   ```bash
   cd /path/to/your/AI-native-textbook/backend
   ```

4. **Initialize project**:
   ```bash
   railway init
   ```

5. **Link to GitHub and set variables**:
   ```bash
   railway link
   railway variables set OPENAI_API_KEY="your_openrouter_api_key"
   railway variables set OPENAI_BASE_URL="https://openrouter.ai/api/v1"
   railway variables set QDRANT_URL="your_qdrant_url"
   railway variables set QDRANT_API_KEY="your_qdrant_api_key"
   railway variables set QDRANT_COLLECTION="project_documents"
   railway variables set NEON_DB_URL="your_neon_db_connection_string"
   railway variables set SECRET_KEY="your_secret_key_here"
   railway variables set DEBUG="false"
   railway variables set LOG_LEVEL="info"
   ```

6. **Deploy**:
   ```bash
   railway up
   ```

## 2. Frontend Deployment to Vercel

### Prerequisites:
- Vercel CLI installed: `npm install -g vercel`
- Or use the web interface at https://vercel.com

### Steps:

1. **Prepare your frontend directory**:
   ```bash
   cd /path/to/your/AI-native-textbook/frontend
   ```

2. **Login to Vercel** (if using CLI):
   ```bash
   vercel login
   ```

3. **Build the project**:
   ```bash
   npm run build
   ```

4. **Deploy**:
   ```bash
   # Using CLI:
   vercel --prod

   # Or use the web interface by connecting your GitHub repo
   ```

5. **Update the proxy configuration**:
   - In the `frontend/vercel.json` file, replace `<YOUR_BACKEND_URL>` with your actual Railway backend URL
   - If you're using the web interface, you can update this file before deploying

6. **Update the docusaurus.config.js**:
   - Replace `https://<your-vercel-url>.vercel.app` with your actual Vercel deployment URL

## 3. Environment Variables Reference

### Backend (Railway) - Required Variables:
- `OPENAI_API_KEY`: Your OpenRouter API key
- `OPENAI_BASE_URL`: `https://openrouter.ai/api/v1`
- `QDRANT_URL`: Your Qdrant database URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION`: Collection name (e.g., `project_documents`)
- `NEON_DB_URL`: Your Neon database connection string
- `SECRET_KEY`: A random secret key for JWT
- `DEBUG`: `false` for production
- `LOG_LEVEL`: `info`

### Frontend (Vercel) - No specific variables needed, but ensure:
- The proxy URL in `vercel.json` points to your backend
- The URL in `docusaurus.config.js` matches your deployment

## 4. Verification Steps

### After Backend Deployment:
1. Visit: `https://<your-backend-url>.railway.app/health`
2. Should return: `{"status": "healthy"}`

### After Frontend Deployment:
1. Visit your Vercel URL
2. Test the chatbot functionality
3. Verify API calls are working through the proxy

## 5. Common Issues and Solutions

### Issue: API calls failing from frontend
**Solution**: Check that the proxy URL in `frontend/vercel.json` matches your backend deployment URL

### Issue: CORS errors
**Solution**: Ensure your backend allows requests from your frontend domain

### Issue: Build failures
**Solution**:
- For backend: Check that the Dockerfile is properly configured
- For frontend: Ensure all dependencies are correctly specified in package.json

## 6. Updating Deployments

### For Railway (Backend):
```bash
# If using CLI:
railway up

# Or push to GitHub and Railway will auto-deploy if connected
```

### For Vercel (Frontend):
```bash
# If using CLI:
vercel

# Or push to GitHub and Vercel will auto-deploy if connected
```

## 7. Monitoring and Logs

### Railway (Backend):
- Access logs through the Railway dashboard
- Monitor resource usage and scale as needed

### Vercel (Frontend):
- Access logs through the Vercel dashboard
- Monitor performance metrics and analytics