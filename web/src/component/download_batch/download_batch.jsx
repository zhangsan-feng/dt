import {Input, Table, message, Button, Tag} from 'antd';
import {useEffect, useLayoutEffect, useRef, useState} from 'react'
import {DownLoadTaskAddApi, DownLoadTaskDelApi, DownLoadTaskApi} from '../../api/api'


const { Search } = Input;


const DownloadBatch = ()=>{
    const [editState, setEditState] = useState(false);
    const [dataSource, setDataSource] = useState([]);

    const [tableHeight, setTableHeight] = useState(() => {
        const content = document.getElementById("layout-content");
        return content ? content.clientHeight - 240 : 500;
    });
    useLayoutEffect(() => {
        const handleResize = () => {
            const content = document.getElementById("layout-content");
            if (content) {setTableHeight(content.clientHeight - 240);}
        };
        window.addEventListener('resize', handleResize);
        return () => {window.removeEventListener('resize', handleResize);};
    }, []);

    const Submit = (value)=>{
        // console.log(value)
        DownLoadTaskAddApi({"link":value}).then(res=>{
            setEditState(true);
            message.warning({content: res.data}).then()
        })
    }

    useEffect(() => {
        DownLoadTaskApi().then(res=>{
            console.log(res)
            setEditState(false);
            setDataSource(res)
        })
    }, [editState]);


    const columns = [
        {title: 'id', dataIndex: 'id', key: 'id'},
        {title: '链接', dataIndex: 'link', key: 'link'},
        {title: '作者', dataIndex: 'author', key: 'author'},
        {title: '用户id', dataIndex: 'user_id', key: 'user_id'},
        {title: '下载', dataIndex: 'total', key: 'total'},
        {title: '状态', dataIndex: 'status', key: 'status', render:(source)=>{
            if (source.status === 0) {
                return <Tag color="blue">等待中</Tag>
            }else {
                return <Tag color="green">下载中</Tag>
            }
            }},
        {width:150, render: (source)=>{
            if(source !== 1){
                return <Button onClick={()=>{
                    DownLoadTaskDelApi({"id":source.id}).then(res=>{
                        message.warning({content: res.data}).then()
                        setEditState(true);
                    })
                }}>删除</Button>
            }
        }},
        {width:150, render: (source)=>{
                if(source !== 1){
                    return <Button>单独下载</Button>
                }
        }},
    ];
    return (
        <div style={{width:"100%",height:"100%"}} >
            <div style={{display:'flex',}}>
                <Search placeholder="添加链接" onSearch={Submit} enterButton="提交" style={{width:600}}/>
                <Search placeholder="搜索"    onSearch={Submit} enterButton="搜索" style={{width:400, marginLeft:20}}/>
                <Button color="cyan" variant="solid" style={{marginLeft:20, width:100}}>
                    开始批量下载
                </Button>
            </div>
            <div style={{marginTop:20}}>
                {
                    dataSource.length !== 0 ?
                        <Table dataSource={dataSource} columns={columns} rowKey="id" scroll={{y: tableHeight}} pagination={{pageSize:500}}/>
                        : <div></div>
                }

            </div>
        </div>
    )
}


export default DownloadBatch