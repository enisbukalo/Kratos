// Production environment (Docker)
export const environment = {
    production: true,
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:9599'  // For local development
        : `http://${window.location.hostname}:9599`  // For Docker/production
};