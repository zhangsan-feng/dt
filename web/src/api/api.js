import {HttpGet, HttpPost,} from './request'



export const ConfigQueryApi = (p)=> HttpGet(`/api/config_query`, p);
export const ConfigEditApi = (p)=> HttpPost(`/api/config_edit`, p);
export const LinkAnalysisApi = (p)=> HttpPost(`/api/link_analysis`, p);
export const FilePreviewApi = (p)=> HttpGet(`/api/preview`, p);

export const DownLoadBatchStartApi = (p)=> HttpPost(`/api/download_batch_start`, p);
export const DownLoadBatchAddApi = (p)=> HttpPost(`/api/download_batch_add`, p);
export const DownLoadBatchDelApi = (p)=> HttpPost(`/api/download_batch_del`, p);
export const DownLoadBatchQueryApi = (p)=> HttpGet(`/api/download_batch_query`, p);

export const DownLoadRecordQueryApi = (p)=> HttpGet(`/api/download_record_query`, p);
export const DownLoadRecordCleanApi = (p)=> HttpPost(`/api/download_record_clean`, p);
export const DownLoadRecordDeleteApi = (p)=> HttpPost(`/api/download_record_delete`, p);

export const DownLoadManagerQueryApi = (p)=> HttpGet(`/api/download_manger_query`, p);
export const DownLoadManagerKillApi = (p)=> HttpPost(`/api/download_manger_kill`, p);

