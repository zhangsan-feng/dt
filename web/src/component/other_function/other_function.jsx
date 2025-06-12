import {Button, Card, Input, Space} from 'antd';
import AdaptiveHeight from '../adaptive_height_hook'
import React,{useState} from "react";


const { TextArea } = Input;
const OtherFunction = ()=>{
    const tableHeight = AdaptiveHeight(100)
    const [TextOut, setTextOut] = useState("NULL")

    return (
        <div style={{height:tableHeight, overflow: 'auto', display: 'flex',}}>
            <div style={{width:"50%"}}>
                <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
                    <Card title="文件操作" >
                        <div style={{display: 'flex', }}>
                            <Button>删除下载文件</Button>
                            <Button>下载文件查重</Button>

                        </div>
                    </Card>

                    <Card title="音频分离/合成" >
                        <div style={{display: 'flex'}}>
                            <p>Card content</p>
                            <p>Card content</p>
                        </div>
                    </Card>
                </Space>
            </div>
            <div style={{marginLeft:"2%", width:"50%"}}>
                <TextArea value={TextOut}  style={{resize:"none", height:tableHeight}} disabled/>
            </div>
        </div>
    )
}

export default OtherFunction;