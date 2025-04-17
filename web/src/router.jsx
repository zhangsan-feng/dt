import { createBrowserRouter, RouteObject } from 'react-router-dom';
import AdminHome from './admin_home/admin_home.jsx'
import DownloadBatch from "./component/download_batch/download_batch.jsx";
import DownloadPreview from "./component/download_preview/download_preview.jsx";
import DownloadRecord from "./component/download_record/download_record.jsx";
import DownloadSettings from "./component/download_settings/download_settings.jsx";
import DownloadWork from "./component/download_work/download_work.jsx";
import OtherFunction from "./component/other_function/other_function.jsx";


const routes = [
  {
    path: "/",
    element: <AdminHome />,
    children: [
      {
        path:"/download_work",
        element:<DownloadWork/>
      },
      {
        path:"/download_batch",
        element:<DownloadBatch/>
      },
      {
        path:"/download_settings",
        element:<DownloadSettings/>
      },
      {
        path:"/download_record",
        element:<DownloadRecord/>
      },
      {
        path:"/download_preview",
        element:<DownloadPreview/>
      },
      {
        path:"/other_function",
        element:<OtherFunction/>
      }
    ]
  },
];

const httpRouter = createBrowserRouter(routes);
export default httpRouter;