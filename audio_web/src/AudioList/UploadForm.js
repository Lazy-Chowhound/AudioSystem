import React from "react";
import {Button, Form, Input, Upload} from "antd";
import {UploadOutlined} from "@ant-design/icons";

class UploadForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            formRef: React.createRef()
        }
    }

    upload = (values) => {
        console.log(values)
    }

    uploadFailed = (errorInfo) => {
        console.log(errorInfo);
    };

    onChange = (file) => {
        console.log(file)
    }

    onReset = () => {
        this.state.formRef.current.resetFields();
    }

    checkSize = () => {
        const formData = this.state.formRef.current.getFieldsValue();
        const size = formData.size;
        if (!size.endsWith("MB") && !size.endsWith("GB")) {
            return Promise.reject("大小只能以GB或者MB结尾")
        }
        return Promise.resolve();
    }

    render() {
        return (
            <Form ref={this.state.formRef} name="uploadForm" labelCol={{span: 8}} wrapperCol={{span: 16}}
                  onFinish={this.upload} onFinishFailed={this.uploadFailed} labelAlign={"left"}
                  autoComplete="off">
                <Form.Item label="数据集名称" name="datasetName"
                           rules={[{required: true, message: "请输入数据集名称"}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="语言" name="language"
                           rules={[{required: true, message: "请输入语言"}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="大小" name="size"
                           rules={[{required: true, message: "请输入大小"}, {validator: this.checkSize}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="时长" name="hour"
                           rules={[{required: true, message: "请输入时长"}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="人数" name="people"
                           rules={[{required: true, message: "请输入人数"}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="格式" name="form"
                           rules={[{required: true, message: "请输入格式"}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="描述" name="description"
                           rules={[{required: true, message: "请输入描述"}]}>
                    <Input.TextArea/>
                </Form.Item>
                {/*todo 上传地址*/}
                <Form.Item label="数据集">
                    <Upload action="https://www.mocky.io/v2/5cc8019d300000980a055e76" directory
                            onChange={this.onChange}>
                        <Button icon={<UploadOutlined/>}>选择数据集</Button>
                    </Upload>
                </Form.Item>
                <Form.Item wrapperCol={{offset: 8, span: 16}}>
                    <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
                        <Button type="primary" htmlType="submit" onClick={this.upload}> 上传 </Button>
                        <Button htmlType="button" onClick={this.onReset}> 重置 </Button>
                    </div>
                </Form.Item>
            </Form>
        )
    }

}

export default UploadForm;