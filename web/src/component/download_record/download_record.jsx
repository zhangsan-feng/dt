import React, {useLayoutEffect, useRef} from 'react';
import { Space, Table } from 'antd';
import {DownLoadRecordDeleteApi, DownLoadRecordQueryApi} from '../../api/api'
import {useState, useEffect} from 'react'
import { Button, Modal, Image } from 'antd';
import ReactPlayer from "react-player";
import './download_record.css'

const LocalizedModal = (source) => {
    const [open, setOpen] = useState(false);
    const [buffered, setBuffered] = useState(0);

    const onProgress = (state) => {setBuffered(state.loadedSeconds / state.duration * 100);};

    const showModal = () => {setOpen(true);};
    const hideModal = () => {setOpen(false);};
    // console.log(source.source.files)
    return (
        <>
            <Button type="primary" onClick={showModal}>预览</Button>
            <Modal
                title={`${source.source.author}-${source.source.desc}`}
                open={open} onOk={hideModal} onCancel={hideModal} width="100%" footer={null}
            >
                <div className="record-container" >
                    <div className="record-container-box">
                        <div className="record-container-box-resource">
                            {
                                source.source.files.split(",").map((items, index) => {
                                    if (items.includes(".png")) {
                                        return <Image key={index} src={items}></Image>
                                    }else if (items.includes(".mp4") || items.includes(".flv") || items.includes(".mp3")) {
                                        return <ReactPlayer url={items} controls={true} width="100%" height="100%" onProgress={onProgress}/>


                                    }
                                })
                            }
                        </div>
                    </div>
                </div>
            </Modal>
        </>
    );
};


const DownloadRecord = ()=>{
    const [data, setData] = useState([]);
    const [tableHeight, setTableHeight] = useState(() => {
        const content = document.getElementById("layout-content");
        return content ? content.clientHeight - 200 : 500;
    });
    useLayoutEffect(() => {
        const handleResize = () => {
            const content = document.getElementById("layout-content");
            if (content) {setTableHeight(content.clientHeight - 200);}
        };
        window.addEventListener('resize', handleResize);
        return () => {window.removeEventListener('resize', handleResize);};
    }, []);

    useEffect(() => {
        DownLoadRecordQueryApi().then(res => setData(res));
        const intervalId = setInterval(() => {DownLoadRecordQueryApi().then(res => setData(res));}, 3000);
        return () => {clearInterval(intervalId);};
    }, []);

    const columns = [
        {title: 'id', dataIndex: 'id', key: 'id', width: 80,ellipsis:true},
        {title: '作品id', dataIndex: 'aweme_id', key: 'aweme_id', width: 200,ellipsis:true},
        {title: '作者', dataIndex: 'author', key: 'author', width: "10%",ellipsis:true},
        {title: '作者id', dataIndex: 'author_id', key: 'author_id',ellipsis:true},
        {title: '文案', key: 'desc', dataIndex: 'desc',ellipsis:true},
        {title: '', key: '', dataIndex: '', width:80, render: (text, source) => {
                return <Button onClick={()=>{
                    DownLoadRecordDeleteApi({"id":source.id}).then(res=>{})
                }}> 删除</Button>
            }
        },
        {title: '', key: '', width:80, render: (_, source) => (
                <Space size="middle">
                    <LocalizedModal source={source}/>
                </Space>
            ),
        },
    ];


    return (
        <div>
            {
                data.length !== 0 ?
                    <Table dataSource={data} columns={columns} rowKey="id" scroll={{y: tableHeight}} pagination={{pageSize:500}}/>
                    : <div></div>
            }
        </div>
    )
}

export default DownloadRecord