import {Input, Table, message, Button, Tag} from 'antd';
import {useEffect, useLayoutEffect, useRef, useState} from 'react'
import {DownLoadBatchAddApi, DownLoadBatchDelApi, DownLoadBatchQueryApi, DownLoadBatchStartApi} from '../../api/api'


const { Search } = Input;


const DownloadBatch = ()=>{

    const [dataSource, setDataSource] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [pageTotal, setPageTotal] = useState(1);

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

    const QueryData = (page=currentPage)=>{
        DownLoadBatchQueryApi({"page":page}).then(res=>{
            setDataSource(res.data);
            setPageTotal((pageTotal)=> pageTotal + res.length + 1);
        })
    }
    const Submit = (value)=>{DownLoadBatchAddApi({"link":value}).then(res=>{message.warning({content: res.data}).then();QueryData()})}
    useEffect(() => {QueryData()}, []);

    const tableChangeHandler = (value)=> {setCurrentPage(value.current);QueryData(value.current)}
    const columns = [
        {title: 'id', dataIndex: 'id', key: 'id'},
        {title: '链接', dataIndex: 'link', key: 'link'},
        {title: '作者', dataIndex: 'author', key: 'author'},
        {title: '作者id', dataIndex: 'user_id', key: 'user_id'},
        {title: '状态', dataIndex: 'status', key: 'status', render:(_, source)=>{
            // console.log(source.status === 0)
            if (source.status === 0) {
                return <Tag color="blue">等待中</Tag>
            }else {
                return <Tag color="green">下载中</Tag>
            }
            }},
        {width:150, render: (_, source)=>{
            if(source !== 1){
                return <Button color="pink"  variant="solid" onClick={()=>{
                    DownLoadBatchDelApi({"id":source.id}).then(res=>{
                        message.warning({content: res.data}).then()
                        QueryData()
                    })
                }}>删除</Button>
            }
        }},
    ];
    return (
        <div style={{width:"100%",height:"100%"}} >
            <div style={{display:'flex',}}>
                <Search placeholder="添加链接" onSearch={Submit} enterButton="提交" style={{width:400}}/>
                {/*<Search placeholder="搜索"    onSearch={Submit} enterButton="搜索" style={{width:400, marginLeft:20}}/>*/}
                <Button color="cyan" variant="solid" style={{marginLeft:20, width:100}} onClick={()=>{
                    DownLoadBatchStartApi().then(res=>{message.warning({content: res.data}).then()})
                }}>
                    开始批量下载
                </Button>
            </div>
            <div style={{marginTop:20}}>
                {
                    dataSource.length !== 0 ?
                        <div>

                            <Table dataSource={dataSource}
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
        </div>
    )
}


export default DownloadBatch