import {DownLoadManagerQueryApi, DownLoadManagerKillApi} from '../../api/api'
import React, {useState, useEffect, useLayoutEffect} from 'react'
import {Button, Space, Table} from "antd";
import AdaptiveHeight from '../adaptive_height_hook'

const DownLoadManager = () => {


    const [data, setData] = useState([]);
    const [pageTotal, setPageTotal] = useState(0);

    const tableHeight = AdaptiveHeight()

    const columns = [
        {title: 'uuid', dataIndex: 'uuid', key: 'uuid', width: 300},
        {title: 'link', dataIndex: 'link', key: 'link', width: 200,ellipsis:true},
        {title: 'status', dataIndex: 'status', key: 'status', width: 100},
        {title: '', key: '', dataIndex: '', width:80, render: (text, source) => {
            if (source.status === '运行中') {
                return <Button onClick={()=>{
                        DownLoadManagerKillApi({"uuid":source.uuid}).then(res=>{})
                    }}> 暂停</Button>
                }
            }
        },
    ];

    useEffect(()=>{DownLoadManagerQueryApi().then(res => {setData(res); setPageTotal(res.length);});}, [])

    useEffect(() => {
        const intervalId = setInterval(() => {DownLoadManagerQueryApi().then(res => setData(res));}, 3000);
        return () => {clearInterval(intervalId);};
    }, []);


    return (
        <div>
            {
                data.length !== 0 ?
                    <Table dataSource={data}
                           columns={columns}
                           rowKey="uuid"
                           scroll={{y: tableHeight}}
                           pagination={{pageSize:500, total:pageTotal}} />
                    : <div></div>
            }
        </div>
    )
}
export default DownLoadManager;