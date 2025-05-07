import {HttpGet, HttpPost,} from './request'



export const ConfigQueryApi = (p)=> HttpGet(`/api/config_query`, p);
export const ConfigEditApi = (p)=> HttpPost(`/api/config_edit`, p);
export const DouYinAnalysisApi = (p)=> HttpPost(`/api/link_analysis`, p);
export const FilePreviewApi = (p)=> HttpGet(`/api/preview`, p);
export const DownLoadTaskAddApi = (p)=> HttpPost(`/api/download_batch_add`, p);
export const DownLoadTaskDelApi = (p)=> HttpPost(`/api/download_batch_del`, p);
export const DownLoadTaskApi = (p)=> HttpGet(`/api/download_batch_query`, p);
export const DownLoadRecordQueryApi = (p)=> HttpGet(`/api/download_record_query`, p);
export const DownLoadRecordDeleteApi = (p)=> HttpPost(`/api/download_record_delete`, p);

