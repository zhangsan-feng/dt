import React, {useLayoutEffect, useRef} from 'react';
import { Space, Table } from 'antd';
import {DownLoadRecordDeleteApi, DownLoadRecordQueryApi} from '../../api/api'
import {useState, useEffect} from 'react'
import { Button, Modal, Image } from 'antd';
import ReactPlayer from "react-player";




const DownloadRecord = ()=>{
    const [data, setData] = useState([]);
    const [dataChange, setDataChange] = useState(false);
    const [tableHeight, setTableHeight] = useState(() => {
        const content = document.getElementById("layout-content");
        return content ? content.clientHeight - 100 : 500;
    });
    useLayoutEffect(() => {
        const handleResize = () => {
            const content = document.getElementById("layout-content");
            if (content) {setTableHeight(content.clientHeight - 100);}
        };
        window.addEventListener('resize', handleResize);
        return () => {window.removeEventListener('resize', handleResize);};
    }, []);
    // setTimeout(()=>{DownLoadRecordQueryApi().then(res=>{setData(res)})}, 3000)
    useEffect(()=>{DownLoadRecordQueryApi().then(res=>{setData(res)})}, [dataChange])

    const LocalizedModal = (source) => {
        const [open, setOpen] = useState(false);
        const showModal = () => {
            setOpen(true);
        };
        const hideModal = () => {
            setOpen(false);
        };
        // console.log(source.source.files)
        return (
            <>
                <Button type="primary" onClick={showModal}>预览</Button>
                <Modal
                    title={`${source.source.author}-${source.source.desc}`}
                    open={open}
                    onOk={hideModal}
                    onCancel={hideModal}
                    width="100%"
                    footer={null}
                >
                    <div className="preview-container" >
                        <div className="container-box">
                            <div className="box-resource">
                                {
                                    source.source.files.split(",").map((items, index) => {
                                        if (items.includes(".png")) {
                                            return <Image key={index} src={items}></Image>
                                        }else{
                                            return <ReactPlayer url={items} controls={true} width="100%" height="100%" playing={false}
                                                                config={{file: {attributes: {preload: 'metadata'}}}}/>

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


    const columns = [
        {title: 'id', dataIndex: 'id', key: 'id', width: 100},
        {title: '作者', dataIndex: 'author', key: 'author',ellipsis:true},
        {title: '作者id', dataIndex: 'author_id', key: 'author_id',ellipsis:true},
        {title: '文案', key: 'desc', dataIndex: 'desc',ellipsis:true},
        {title: '', key: '', dataIndex: '', width:100, render: (text, source) => {
                return <Button onClick={()=>{
                    DownLoadRecordDeleteApi({"id":source.id}).then(res=>{
                        setDataChange(true)
                    })
                }}> 删除</Button>
            }
        },
        {title: '', key: '', width:100, render: (_, source) => (
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