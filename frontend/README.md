# Collink Frontend

A beautiful, modern React/Next.js frontend for the Collink college prediction platform.

## 🚀 Features

- **Modern UI/UX**: Beautiful, responsive design with smooth animations
- **College Predictions**: Get accurate predictions based on exam rank
- **Smart Search**: Advanced search with filters and suggestions
- **Detailed Insights**: Comprehensive college information with ratings, fees, placements
- **Real-time Data**: Connected to the Collink backend API
- **Mobile Responsive**: Works perfectly on all devices

## 🛠️ Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **React Query**: Data fetching and caching
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API calls

## 📦 Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Connection

Make sure the Collink backend is running on port 8000:

```bash
# In the backend directory
python main.py
```

## 📱 Pages & Components

### Pages
- **Home** (`/`): Landing page with hero section and features
- **Predict** (`/predict`): College prediction form and results
- **Search** (`/search`): College search with filters
- **Colleges** (`/colleges`): Browse all colleges
- **College Details** (`/college/[name]`): Detailed college information

### Components
- **Header**: Navigation with responsive mobile menu
- **Hero**: Stunning landing page hero section
- **PredictionForm**: Interactive form for college predictions
- **PredictionResults**: Beautiful results display with confidence levels
- **SearchForm**: Advanced search with filters
- **CollegeCard**: Individual college display cards

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (`#3b82f6` to `#8b5cf6`)
- **Secondary**: Purple gradient (`#8b5cf6` to `#ec4899`)
- **Success**: Green (`#10b981`)
- **Warning**: Yellow (`#f59e0b`)
- **Error**: Red (`#ef4444`)

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800

### Animations
- **Fade In**: Smooth opacity transitions
- **Slide Up**: Vertical slide animations
- **Hover Effects**: Interactive hover states
- **Loading States**: Spinner animations

## 🔌 API Integration

The frontend connects to the Collink backend API with the following endpoints:

### Core Endpoints
- `GET /api/v1/health` - Health check
- `GET /api/v1/exams` - Get supported exams
- `POST /api/v1/predict` - Get college predictions
- `GET /api/v1/search` - Search colleges
- `GET /api/v1/college/{name}` - Get college details

### Enhanced Endpoints
- `GET /api/v1/college/{name}/insights` - Comprehensive college insights
- `GET /api/v1/college/{name}/ratings` - Detailed ratings
- `GET /api/v1/college/{name}/fees` - Fee structure
- `GET /api/v1/college/{name}/placement` - Placement statistics

## 📊 Data Flow

1. **User Input**: User enters exam rank and preferences
2. **API Call**: Frontend sends request to backend
3. **Data Processing**: Backend processes rank and returns predictions
4. **Results Display**: Frontend displays results with confidence levels
5. **College Details**: Users can view detailed college information

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect to GitHub**:
   ```bash
   git add .
   git commit -m "Initial frontend commit"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Connect your GitHub repository to Vercel
   - Set environment variables
   - Deploy automatically

### Manual Deployment

1. **Build the project**:
   ```bash
   npm run build
   ```

2. **Start production server**:
   ```bash
   npm start
   ```

## 🔧 Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Code Structure

```
frontend/
├── components/          # Reusable components
├── lib/                # Utilities and API client
├── pages/              # Next.js pages
├── styles/             # Global styles
├── public/             # Static assets
└── package.json        # Dependencies
```

## 🎯 Features Overview

### College Predictions
- **Multi-Exam Support**: JEE Advanced, NEET UG, IELTS
- **Confidence Levels**: High, Medium, Low confidence indicators
- **Rank Analysis**: Visual comparison of your rank vs closing rank
- **Category Support**: General, OBC, SC, ST, EWS categories

### College Search
- **Fuzzy Search**: Find colleges by partial name
- **Exam Filtering**: Filter by specific exams
- **Location Search**: Search by college location
- **Advanced Filters**: Multiple filter options

### College Insights
- **NIRF Rankings**: Official Indian rankings
- **World Rankings**: International university rankings
- **Detailed Ratings**: Academics, Campus, Placements, ROI
- **Fee Structure**: Complete fee breakdown
- **Placement Stats**: Average package, highest package, recruiters
- **Pros & Cons**: Detailed analysis of each college

## 🎨 UI/UX Highlights

- **Responsive Design**: Works on all screen sizes
- **Smooth Animations**: Framer Motion powered transitions
- **Modern Gradients**: Beautiful color gradients throughout
- **Interactive Elements**: Hover effects and micro-interactions
- **Loading States**: Proper loading indicators
- **Error Handling**: User-friendly error messages
- **Accessibility**: WCAG compliant design

## 🔗 Backend Integration

The frontend is designed to work seamlessly with the Collink backend:

- **Real-time Data**: Live connection to backend API
- **Error Handling**: Graceful error handling for API failures
- **Loading States**: Proper loading indicators during API calls
- **Data Validation**: Client-side validation before API calls
- **Caching**: React Query for efficient data caching

## 📈 Performance

- **Optimized Images**: Next.js Image optimization
- **Code Splitting**: Automatic code splitting by Next.js
- **Lazy Loading**: Components load on demand
- **Caching**: React Query for API response caching
- **Bundle Optimization**: Optimized bundle size

## 🛡️ Security

- **API Proxy**: Next.js rewrites for API calls
- **Input Validation**: Client-side validation
- **Error Boundaries**: React error boundaries
- **Secure Headers**: Next.js security headers

## 🎉 Getting Started

1. **Clone the repository**
2. **Install dependencies**: `npm install`
3. **Start backend**: `python main.py` (in backend directory)
4. **Start frontend**: `npm run dev`
5. **Open browser**: Navigate to `http://localhost:3000`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Collink Frontend** - Your gateway to finding the perfect college match! 🎓✨ 