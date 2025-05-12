# AI Chat Backend

A Flask-based backend service for an AI chat application using Google's Gemini API, MongoDB for data persistence, and JWT for authentication.

## Features

- User authentication with JWT
- Chat history management
- Integration with Google's Gemini AI model
- MongoDB database storage
- CORS support

## Prerequisites

- Python 3.x
- MongoDB running locally or a MongoDB Atlas connection string
- Google Gemini API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file in the root directory with the following variables:
```env
apiKey=your_gemini_api_key
JWT_SECRET_KEY=your_jwt_secret
```

4. Start the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Documentation

Detailed API documentation can be found in [API_DOCS.md](API_DOCS.md)

## Project Structure

```
├── controllers/         # Route handlers
├── middleware/          # Authentication middleware
├── models/             # Database models
├── .env                # Environment variables
├── .gitignore         # Git ignore rules
├── API_DOCS.md        # API documentation
├── app.py             # Application entry point
├── requirements.txt    # Python dependencies
└── utils.py           # Utility functions
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details