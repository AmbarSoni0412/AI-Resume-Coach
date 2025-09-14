# Deployment Guide

This guide covers deploying the Resume Coach app to various cloud platforms.

## Quick Deploy Options

### 1. Streamlit Cloud (Easiest)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository and branch
   - Set environment variables:
     - `GOOGLE_API_KEY`: Your Google AI API key
   - Click "Deploy!"

**Pros**: Free, automatic deployments, built-in HTTPS
**Cons**: Limited customization

### 2. Railway (Recommended for Beginners)

1. **Connect GitHub**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure Environment**
   - Add environment variable: `GOOGLE_API_KEY`
   - Railway automatically detects it's a Streamlit app

3. **Deploy**
   - Railway will automatically deploy and provide a URL

**Pros**: Simple, good free tier, automatic deployments
**Cons**: Limited free tier

### 3. Render

1. **Create Web Service**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Choose "Web Service"

2. **Configure**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Environment: `GOOGLE_API_KEY`

3. **Deploy**
   - Click "Create Web Service"

**Pros**: Good free tier, automatic deployments
**Cons**: Cold starts on free tier

### 4. Heroku

1. **Install Heroku CLI**

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_api_key_here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

**Pros**: Mature platform, many add-ons
**Cons**: No free tier anymore

### 5. Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t resume-coach .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key resume-coach
   ```

3. **Deploy to Cloud**
   - Push to Docker Hub
   - Deploy on any cloud provider that supports Docker

## Environment Variables

### Required
- `GOOGLE_API_KEY`: Your Google AI API key

### Optional
- `RAZORPAY_KEY_ID`: For payment integration
- `RAZORPAY_KEY_SECRET`: For payment integration
- `ANALYSIS_PRICE_INR`: Price for analysis

## System Requirements

- Python 3.8+
- Poppler (for PDF processing)
- At least 512MB RAM
- 1GB disk space

## Performance Optimization

1. **File Size Limits**
   - PDF files limited to 10MB
   - Only first page processed

2. **Rate Limiting**
   - 5-second minimum between requests
   - Automatic retry with exponential backoff

3. **Caching**
   - Session state management
   - Efficient image processing

## Monitoring and Logs

The app includes logging for:
- PDF processing errors
- API quota issues
- General application errors

Check your platform's logging system for debugging.

## Troubleshooting

### Common Issues

1. **"Poppler not found"**
   - Ensure poppler is installed on the system
   - For Docker: Already included in Dockerfile

2. **"API quota exceeded"**
   - Wait for quota reset
   - Consider upgrading Google AI plan

3. **"File too large"**
   - Reduce PDF file size
   - Use PDF compression tools

4. **App won't start**
   - Check environment variables
   - Verify all dependencies are installed

### Getting Help

1. Check the logs in your deployment platform
2. Verify environment variables are set correctly
3. Test locally first
4. Check Google AI API key permissions

## Security Considerations

1. **API Keys**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **File Uploads**
   - File size limits implemented
   - Only PDF files accepted
   - Temporary processing only

3. **Rate Limiting**
   - Built-in rate limiting
   - Session-based protection

## Scaling Considerations

For high traffic:
1. Consider upgrading Google AI plan
2. Implement caching layer
3. Use load balancing
4. Consider paid hosting tiers
