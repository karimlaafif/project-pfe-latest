<div align="center">

# 🛡️ LendGuard 

### AI-Powered Loan Intelligence Platform

**Stop Fraud. Approve More Loans. In Real-Time.**
A comprehensive AI-powered platform for loan default prediction, fraud detection, and Governance, Risk & Compliance (GRC) management.

[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[🚀 Live Demo]((https://drive.google.com/file/d/1vY34zuu-Ep2CefC7bLwwLehWubuA1Z0O/view?usp=sharing)) • [📖 Documentation](https://docs.lendguard.ai) • [🎥 Video Tour]((https://drive.google.com/file/d/1vY34zuu-Ep2CefC7bLwwLehWubuA1Z0O/view?usp=sharing)) • [💬 Community](https://discord.gg/techevolab)

![LendGuard AI Dashboard](https://via.placeholder.com/1200x600/0EA5E9/ffffff?text=LendGuard+AI+Dashboard)

</div>

---



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

For support, email techevo.63@gmail.com or open an issue on GitHub.


## 📊 Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/karimlaafif/lendguard-ai?style=social)
![GitHub forks](https://img.shields.io/github/forks/karimlaafif/lendguard-ai?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/karimlaafif/lendguard-ai?style=social)
![GitHub contributors](https://img.shields.io/github/contributors/karimlaafif/lendguard-ai)

![GitHub issues](https://img.shields.io/github/issues/karimlaafif/lendguard-ai)
![GitHub pull requests](https://img.shields.io/github/issues-pr/karimlaafif/lendguard-ai)
![GitHub last commit](https://img.shields.io/github/last-commit/karimlaafif/lendguard-ai)
![GitHub code size](https://img.shields.io/github/languages/code-size/karimlaafif/lendguard-ai)

</div>

---

## 🌟 Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=karimlaafif/lendguard-ai&type=Date)](https://star-history.com/#karimlaafif/lendguard-ai&Date)

</div>

---

<div align="center">

### Made with ❤️ by the LendGuard Team

**[Website](https://lendguard.ai)** • **[Documentation](https://docs.lendguard.ai)** • **[API](https://api.lendguard.ai)** • **[Blog](https://blog.lendguard.ai)**
