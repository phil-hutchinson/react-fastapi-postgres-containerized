// API configuration
const getApiBaseUrl = () => {
  const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
  if (!apiBaseUrl) {
    throw new Error('REACT_APP_API_BASE_URL environment variable is not set. Please configure the API base URL.');
  }
  return apiBaseUrl;
};

const config = {
  apiBaseUrl: getApiBaseUrl(),
};

export default config;
