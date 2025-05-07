import './main.css';
import { RouterProvider } from 'react-router-dom';
import httpRouter from './router.jsx';
import ReactDOM from 'react-dom/client';
import '@ant-design/v5-patch-for-react-19';

const rootElement = document.getElementById('root');
if (!rootElement) {
    throw new Error('Failed to find the root element');
}
ReactDOM.createRoot(rootElement).render(
    <RouterProvider router={httpRouter} />
);


// https://animejs.com/documentation/animation