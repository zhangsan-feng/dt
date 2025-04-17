
import {Input, Button, Form, Select} from 'antd';
import React from 'react';
import {DouYinAnalysisApi,} from "../../api/api";




const DownloadWork = ()=>{
    const [form] = Form.useForm();
    const onFinish = ( values ) => {
        DouYinAnalysisApi(values).then(res=>{
            console.log(res)
        })
    };


    return (
        <div style={{marginTop: "2%", marginLeft: "10%", marginRight: "10%", height: "100%",}}>
            <div>
                <Form form={form} onFinish={onFinish}  >
                    <Form.Item  name="link" ><Input placeholder="视频下载"style={{resize:"none", height:50}}/></Form.Item>
                    <Form.Item style={{display: 'flex', justifyContent: 'center'}}>
                        <Button type="primary" htmlType="submit" style={{width: 150}}>下载</Button>
                    </Form.Item>

                </Form>

                {/*<Form form={form} onFinish={onFinish}  >*/}
                {/*    <Form.Item  name="link" ><Input placeholder="评论下载"style={{resize:"none", height:50}}/></Form.Item>*/}
                {/*    <Form.Item style={{display: 'flex', justifyContent: 'center'}}>*/}
                {/*        <Button type="primary" htmlType="submit" style={{width: 150}}>下载</Button>*/}
                {/*    </Form.Item>*/}
                {/*</Form>*/}
            </div>
        </div>
    )
}

export default DownloadWork