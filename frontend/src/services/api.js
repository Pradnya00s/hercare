import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    
  },
});

// Request interceptor to add JWT token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // 🔥 Important: don't override multipart headers
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('http://127.0.0.1:8000/api/auth/token/refresh/', 
          {
          refresh: refreshToken,
          }
      );

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  getProfile: () => api.get('/auth/profile/'),
};

// Dashboard API
export const dashboardAPI = {
  getDashboard: () => api.get('/dashboard/'),
};

export const periodTrackerAPI = {
  logEntry: (data) => api.post('/auth/profile/period-log/', data),
  getHistory: () => api.get('/auth/profile/period-history/'),
  getPrediction: () => api.get('/period/prediction/'),
  getPhase: () => api.get('/period/phase/'),
  getIrregularity: () => api.get('/period/irregularity/'),
  deleteEntry: (id) => api.delete(`/period/delete/${id}/`)
};

export const chatAPI = {
  sendMessage: (data) => api.post("/chat/", data),
  getHistory: () => api.get("/chat/history/"),
};

export const breastCancerAPI = {
  saveResult: (data) => api.post('/auth/profile/breast-cancer/', data),
  getHistory: () => api.get('/auth/profile/breast-cancer/'),
};

export const pcosAPI = {
  predictSymptoms: (data) => api.post('/pcos/form-predict/', data),
  uploadUltrasound: (formData) => {
    return api.post('/ultrasound/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getCombinedPrediction: (data) => api.post('/combined-prediction/', data),
  getHistory: () => api.get('/auth/profile/pcos-history/'),
};

export const oncologyAPI = {
  fullAssessment: (formData) => {
    return api.post('/breast/full-assessment/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export default api;
