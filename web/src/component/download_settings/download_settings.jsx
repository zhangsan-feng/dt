
import  { useState, useEffect } from 'react';
import { Button, Form, Input, Radio } from 'antd';
import {ConfigEditApi, ConfigQueryApi} from "../../api/api.js";

const DownloadSettings = ()=>{
    const [form] = Form.useForm();
    useEffect(() => {
        ConfigQueryApi({}).then(res=>{
            form.setFieldsValue({"douyin_cookie":res.data.douyin_cookie})
            form.setFieldsValue({"save_path":res.data.save_path})
            console.log(res)
        })
    }, []);
    const onFinish = (values) => {
        ConfigEditApi(values).then(res=>{
            console.log(res)
        })
      console.log('Success:', values);
    };


    return (
        <div style={{marginTop:"2%"}}>
            <Form  onFinish={onFinish} form={form} labelCol={{ span: 4 }} wrapperCol={{ span: 16 }}>
                <Form.Item label="douyin_cookie" name="douyin_cookie"><Input placeholder="" /></Form.Item>
                <Form.Item label="代理" name="proxy"><Input placeholder="" /></Form.Item>
                {/*<Form.Item label="下载路径" name="save_path"><Input placeholder="" /></Form.Item>*/}
                <Form.Item style={{ display: 'flex', justifyContent: 'center' }}>
                    <Button type="primary" htmlType="submit"  style={{ width: 300 }}>提交修改</Button>
                </Form.Item>
            </Form>

        </div>
    )
}

export default DownloadSettings