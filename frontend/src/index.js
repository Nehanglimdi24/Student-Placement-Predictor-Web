import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { GoogleOAuthProvider } from '@react-oauth/google';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <GoogleOAuthProvider clientId="598611898757-juf16mj7umio8jup0jfbuda1tmbdadvv.apps.googleusercontent.com">
    <App />
  </GoogleOAuthProvider>
);
