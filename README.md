# LendGuard AI - Intelligent Loan Risk Assessment Platform

A comprehensive AI-powered platform for loan default prediction, fraud detection, and Governance, Risk & Compliance (GRC) management.

## 🌟 Features

### Core Functionality
- **Loan Default Prediction**: Machine learning models to assess loan default risk
- **Fraud Detection**: Advanced algorithms to identify potentially fraudulent loan applications
- **GRC Framework**: Comprehensive governance, risk, and compliance management dashboard
- **Risk Scoring**: Intelligent risk assessment and scoring system
- **Real-time Analytics**: Interactive dashboards and data visualizations

### Technical Features
- Multi-language support (English, French, Arabic)
- Dark/Light theme support
- Responsive design for all devices
- Real-time data processing
- Secure authentication with Auth.js
- RESTful API architecture

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes, Prisma ORM
- **Database**: PostgreSQL
- **Data Warehouse**: ClickHouse (Bronze/Silver/Gold architecture)
- **ML Models**: Python (scikit-learn, pandas, numpy)
- **Authentication**: Auth.js (NextAuth.js v5)
- **UI Components**: shadcn/ui, Recharts

### Project Structure
```
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── dashboard/         # Dashboard pages
│   └── [locale]/          # Internationalized pages
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   └── dashboard/        # Dashboard-specific components
├── lib/                   # Utility functions
├── prisma/               # Database schema & migrations
├── models/               # ML model files
├── scripts/              # Utility scripts
├── warehouse/            # Data warehouse configuration
└── public/               # Static assets
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- PostgreSQL 14+
- Python 3.9+
- ClickHouse (optional, for data warehouse)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/karimlaafif/pfe.git
   cd pfe
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and configure:
   - Database connection (PostgreSQL)
   - Authentication secrets
   - API endpoints
   - ClickHouse connection (if using data warehouse)

4. **Set up the database**
   ```bash
   npx prisma migrate dev
   npx prisma generate
   ```

5. **Seed the database (optional)**
   ```bash
   npm run seed
   ```

6. **Run the development server**
   ```bash
   npm run dev
   ```

7. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📊 Data Warehouse

The project includes a ClickHouse-based data warehouse with a Bronze/Silver/Gold architecture:

- **Bronze Layer**: Raw data ingestion
- **Silver Layer**: Cleaned and validated data
- **Gold Layer**: Business-ready aggregated metrics

See `warehouse/` directory for configuration and ETL scripts.

## 🤖 Machine Learning Models

The platform uses several ML models:

1. **Loan Default Prediction**: Ensemble model combining Random Forest and XGBoost
2. **Fraud Detection**: Anomaly detection using Isolation Forest and neural networks
3. **Risk Scoring**: Multi-factor risk assessment algorithm

Notebooks for model development are available in `Nootbooks/` directory.

## 📚 Documentation

- [Academic Justification](./ACADEMIC_JUSTIFICATION.md) - ML algorithms and theoretical foundations
- [Authentication Setup](./AUTH_SETUP.md) - Auth.js configuration guide
- [Datasets Guide](./DATASETS_GUIDE.md) - Data sources and processing
- [Design System](./DESIGN_SYSTEM.md) - UI/UX guidelines
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md) - Development progress
- [Quick Reference](./QUICK_REFERENCE.md) - Common commands and workflows

## 🔐 Security

- Secure authentication with Auth.js
- Environment variable protection
- SQL injection prevention via Prisma ORM
- XSS protection with Content Security Policy
- HTTPS enforced in production

## 🌐 Internationalization

The platform supports multiple languages:
- English (en)
- French (fr)
- Arabic (ar)

Language files are located in `messages/` directory.

## 🧪 Testing

```bash
# Run tests
npm test

# Run linting
npm run lint

# Type checking
npm run type-check
```

## 📦 Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Docker
```bash
docker build -t lendguard-ai .
docker run -p 3000:3000 lendguard-ai
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Karim Laafif** - [GitHub](https://github.com/karimlaafif)

## 🙏 Acknowledgments

- Data sources: Lending Club, IEEE-CIS Fraud Detection, FRED Economic Data
- UI components: shadcn/ui
- ML libraries: scikit-learn, TensorFlow, PyTorch

## 📞 Support

For support, email support@lendguard.ai or open an issue on GitHub.

---

**Built with ❤️ for smarter lending decisions**
