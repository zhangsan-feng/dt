import React, {useLayoutEffect, useRef} from 'react';
import { Space, Table } from 'antd';
import {DownLoadRecordDeleteApi, DownLoadRecordQueryApi, DownLoadRecordCleanApi} from '../../api/api'
import {useState, useEffect} from 'react'
import { Button, Modal, Image, Input } from 'antd';
import ReactPlayer from "react-player";
import './download_record.css'

const {Search} = Input

const LocalizedModal = (source) => {
    const [open, setOpen] = useState(false);

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
                                        return <ReactPlayer url={items} controls={true} width="100%" height="100%"/>
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
    const [currentPage, setCurrentPage] = useState(1);
    const [pageTotal, setPageTotal] = useState(1);

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

    const QueryData = (page=currentPage)=>{
        DownLoadRecordQueryApi({"page":page}).then(res => {
            setData(res);
            setPageTotal((pageTotal)=> pageTotal + res.length + 1);
        });
    }
    useEffect(() => {QueryData()}, []);
    useEffect(() => {
        if (currentPage === 1) {
            const intervalId = setInterval(() => {
                    DownLoadRecordQueryApi({"page":currentPage}).then(res => {setData(res)});
                }, 3000);
            return () => clearInterval(intervalId);
        }
    }, [currentPage]);

    const tableChangeHandler = (value)=> {setCurrentPage(value.current); QueryData(value.current)}

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

    const RecordCleanButton = ()=>{
        DownLoadRecordCleanApi().then(res => { QueryData()})

    }

    return (
        <div>

            {
                data.length !== 0 ?
                    <div>
                        <div>
                            <Search style={{width:500}}></Search>
                            <Button style={{marginLeft:20}} onClick={RecordCleanButton}>清空历史记录</Button>
                        </div>
                        <Table dataSource={data}
                               columns={columns}
                               rowKey="id"
                               scroll={{y: tableHeight}}
                               pagination={{pageSize:100, total:pageTotal}}
                               onChange={tableChangeHandler}
                        />
                    </div>
                    : <div></div>
            }
        </div>
    )
}

export default DownloadRecord