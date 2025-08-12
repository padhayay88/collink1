# Collink - College Predictor API

A comprehensive FastAPI backend for predicting colleges based on competitive exam ranks (JEE, NEET, IELTS) with detailed college information, pros/cons, and search functionality.

## 🎯 Features

- **Rank-based College Prediction**: Get college suggestions based on your rank and exam
- **Multi-Exam Support**: JEE Advanced, NEET UG, IELTS
- **College Details**: Comprehensive information including pros, cons, overview
- **Search Functionality**: Fuzzy search for colleges with suggestions
- **Real Data Structure**: Ready for real cutoff data integration
- **RESTful API**: Clean, documented API endpoints

## 🏗️ Architecture

```
collink/
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── routers/                # API route handlers
│   ├── __init__.py
│   ├── predict.py          # Prediction endpoints
│   ├── college.py          # College details endpoints
│   └── search.py           # Search functionality
├── utils/                  # Core logic
│   ├── __init__.py
│   └── match_logic.py      # College prediction algorithm
└── data/                   # Data files
    ├── jee_cutoffs.json    # JEE cutoff data
    ├── neet_cutoffs.json   # NEET cutoff data
    ├── ielts_cutoffs.json  # IELTS cutoff data
    └── college_info.json   # College details and reviews
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd collink
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/api/v1/health

## 📚 API Endpoints

### Core Endpoints

#### 1. Predict Colleges
```http
POST /api/v1/predict
```
**Request Body:**
```json
{
  "exam": "jee",
  "rank": 100,
  "category": "General",
  "gender": "All",
  "quota": "All India"
}
```

#### 2. Get College Details
```http
GET /api/v1/college/{college_name}
```

#### 3. Search Colleges
```http
GET /api/v1/search?query={college_name}&exam={exam_type}&limit={limit}
```

#### 4. Get All Colleges
```http
GET /api/v1/colleges?exam={exam_type}&limit={limit}
```

#### 5. Get Supported Exams
```http
GET /api/v1/exams
```

### Additional Endpoints

- `GET /api/v1/search/suggestions` - Get search suggestions
- `GET /api/v1/search/popular` - Get popular colleges
- `GET /api/v1/college/{college_name}/cutoffs` - Get college cutoffs

## 📊 Data Structure

### Cutoff Data Format
```json
{
  "college": "IIT Bombay",
  "branch": "Computer Science and Engineering",
  "opening_rank": 1,
  "closing_rank": 66,
  "category": "General",
  "quota": "All India",
  "location": "Mumbai, Maharashtra",
  "exam_type": "jee",
  "year": 2023,
  "last_updated": "2023-12-01T00:00:00Z"
}
```

### College Info Format
```json
{
  "name": "IIT Bombay",
  "overview": "Detailed college overview...",
  "pros": ["Excellent placement record", "Strong alumni network"],
  "cons": ["High cost of living", "Intense academic pressure"],
  "location": "Mumbai, Maharashtra",
  "established": 1958,
  "nirf_rank": 3,
  "website": "https://www.iitb.ac.in",
  "contact": {
    "phone": "+91-22-25722545",
    "email": "info@iitb.ac.in",
    "address": "Powai, Mumbai - 400076, Maharashtra"
  },
  "facilities": ["Modern laboratories", "Central library"],
  "placement_stats": {
    "average_package": 1200000,
    "highest_package": 5000000,
    "placement_percentage": 85,
    "top_recruiters": ["Google", "Microsoft", "Amazon"]
  },
  "courses_offered": ["Computer Science and Engineering", "Electrical Engineering"]
}
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## 📈 Adding Real Data

### 1. JEE Data Sources
- **JoSAA**: https://josaa.nic.in
- **College Pravesh**: https://collegepravesh.com
- **Official JEE Advanced**: https://jeeadv.ac.in

### 2. NEET Data Sources
- **MCC**: https://mcc.nic.in
- **AIIMS**: https://www.aiims.edu
- **JIPMER**: https://jipmer.edu.in

### 3. IELTS Data Sources
- **University Websites**: Direct from international universities
- **Shiksha**: https://www.shiksha.com
- **Official IELTS**: https://www.ielts.org

### 4. College Information Sources
- **NIRF**: https://www.nirfindia.org
- **Shiksha**: https://www.shiksha.com
- **Careers360**: https://www.careers360.com
- **Quora/Reddit**: Student reviews and experiences

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment
1. **Render**: Connect GitHub repository
2. **Railway**: Deploy with one-click
3. **Fly.io**: Use Docker deployment
4. **Heroku**: Add Procfile and deploy

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 Testing

### Manual Testing
```bash
# Test prediction endpoint
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"exam": "jee", "rank": 100, "category": "General"}'

# Test search endpoint
curl "http://localhost:8000/api/v1/search?query=IIT&limit=5"

# Test college details
curl "http://localhost:8000/api/v1/college/IIT%20Bombay"
```

### Automated Testing
```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

## 📝 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [link-to-docs]

## 🔮 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Real-time data scraping
- [ ] Machine learning predictions
- [ ] Mobile app API
- [ ] Admin panel
- [ ] Analytics dashboard
- [ ] User authentication
- [ ] College comparison features

---

**Built with ❤️ for students seeking the perfect college match** 