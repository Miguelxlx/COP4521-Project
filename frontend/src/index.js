import React from 'react';
import App from './App';
import ReactDOM from 'react-dom';
import HomeScreen from './screens/HomeScreen';
import LoginScreen from './screens/LoginScreen';
import { 
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider } from 'react-router-dom';
import reportWebVitals from './reportWebVitals';
import { Provider } from 'react-redux';
import { HelmetProvider } from 'react-helmet-async';
import store from './store';




const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path="/" element={<App />}>
            <Route index={true} path="/" element={<HomeScreen />} />
            <Route path="/login" element={<LoginScreen />} />
        </Route>
    )
)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <HelmetProvider>
    <Provider store={store}>
        <RouterProvider router={router} />
    </Provider>
    </HelmetProvider>
  </React.StrictMode>
);

  reportWebVitals();