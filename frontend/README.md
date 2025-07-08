# Agentic Architect Frontend

React-based frontend for the Agentic Architect platform - an AI-powered architecture consulting system that provides expert guidance on system design with comprehensive explanations and business insights.

## Tech Stack

- **Runtime**: Node.js (v18+ recommended)
- **Framework**: React 19.1.0
- **Language**: TypeScript
- **Build Tool**: Create React App 5.0.1
- **Routing**: React Router DOM 7.6.3
- **Styling**: Styled Components 6.1.19
- **HTTP Client**: Axios 1.10.0
- **Visualization**: D3.js 7.9.0, Mermaid 11.8.0
- **Testing**: React Testing Library, Jest

## Prerequisites

- Node.js 18+
- npm or yarn
- Backend service running (default: http://localhost:3001)

## Installation

1. **Clone the repository and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```env
   # API Configuration
   REACT_APP_API_URL=http://localhost:3001/api
   
   # App Configuration
   REACT_APP_NAME="Agentic Architect"
   REACT_APP_VERSION="1.0.0"
   
   # Development
   GENERATE_SOURCEMAP=true
   ```

## Running the Application

### Development Mode
```bash
npm start
```
The application will start on `http://localhost:3000` with hot reloading enabled.

### Alternative Port
To run on a different port (e.g., 3003):
```bash
PORT=3003 npm start
```

### Production Build
```bash
# Build the application
npm run build

# Serve the build (requires serve package)
npx serve -s build -l 3000
```

## Available Scripts

- `npm start` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm test` - Run tests in interactive watch mode
- `npm run eject` - Eject from Create React App (irreversible)

## Features

### Core Functionality
- **Landing Page** - Project requirements input form
- **Conversation Interface** - Interactive chat with AI agents
- **Architecture Visualization** - Visual representation of system designs
- **Documentation Panel** - Generated architecture documentation
- **Real-time Updates** - Live conversation updates and progress tracking

### User Interface Components
- **ConversationPanel** - Main chat interface
- **DocumentationPanel** - Architecture documentation display
- **VisualizationPanel** - System architecture diagrams
- **LandingPage** - Initial project setup form
- **ConversationPage** - Main application interface

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ConversationPanel.tsx
│   ├── DocumentationPanel.tsx
│   └── VisualizationPanel.tsx
├── pages/              # Page components
│   ├── LandingPage.tsx
│   └── ConversationPage.tsx
├── services/           # API and external services
│   └── api.ts
├── types/              # TypeScript type definitions
│   └── index.ts
├── utils/              # Utility functions
├── App.tsx             # Main application component
├── index.tsx           # Application entry point
└── index.css           # Global styles
```

## API Integration

The frontend communicates with the backend through a centralized API service:

### Authentication
- JWT token-based authentication
- Automatic token management
- Login/logout functionality

### Conversations
- Start new architecture consultations
- Send messages to AI agents
- Receive real-time responses
- View conversation history

### Configuration
Update the API base URL in `.env`:
```env
REACT_APP_API_URL=http://localhost:3001/api
```

## Environment Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API endpoint | http://localhost:3001/api |
| `REACT_APP_NAME` | Application name | "Agentic Architect" |
| `REACT_APP_VERSION` | Application version | "1.0.0" |
| `PORT` | Development server port | 3000 |
| `GENERATE_SOURCEMAP` | Generate source maps | true |

## Testing

Run the test suite:
```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false
```

### Test Structure
- **Unit Tests** - Component and utility function tests
- **Integration Tests** - API service tests
- **User Event Tests** - User interaction testing

## Styling

The application uses Styled Components for styling:

### Theme System
- Consistent color palette
- Typography scale
- Spacing system
- Responsive breakpoints

### Component Styling
- Styled Components for component-specific styles
- Global CSS for base styles
- CSS-in-JS for dynamic styling

## Visualization

### D3.js Integration
- Custom architecture diagrams
- Interactive system visualizations
- Data-driven graphics

### Mermaid Diagrams
- Flowcharts and sequence diagrams
- Architecture documentation
- Process visualization

## Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure backend is running on correct port
   - Check REACT_APP_API_URL in .env file
   - Verify CORS configuration in backend

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
   - Check TypeScript errors: `npx tsc --noEmit`

3. **Port Already in Use**
   - Use different port: `PORT=3003 npm start`
   - Kill existing process: `lsof -ti:3000 | xargs kill -9`

4. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token format
   - Verify backend authentication endpoints

### Development Tips

1. **Hot Reloading**
   - Changes to src/ files trigger automatic reload
   - CSS changes apply without full reload

2. **Debugging**
   - Use React Developer Tools browser extension
   - Check browser console for errors
   - Use network tab to monitor API calls

3. **Performance**
   - Use React.memo for expensive components
   - Implement proper key props for lists
   - Monitor bundle size with `npm run build`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Notes

- The application uses React 19 with concurrent features
- TypeScript strict mode is enabled
- ESLint configuration follows React best practices
- Styled Components provide CSS-in-JS styling
- Axios interceptors handle authentication and error management
- React Router provides client-side routing
