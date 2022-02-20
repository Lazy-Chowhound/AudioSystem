import React from "react";
import {Button, Form, Input, Upload, message} from "antd";
import {UploadOutlined} from "@ant-design/icons";
import {sendFile, sendGet} from "../Util/axios";

class UploadForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            formRef: React.createRef(),
            uploading: false,
            fileList: [],
        }
    }

    upload = (values) => {
        this.setState({
            uploading: true
        })
        const dataset = values['datasetName']
        const language = values['language']
        const size = values['size']
        const hour = values['hour']
        const people = values["people"]
        const form = values['form']
        const description = values['description']
        sendGet("/uploadDatasetDescription", {
            params: {
                dataset: dataset,
                language: language,
                size: size,
                hour: hour,
                people: people,
                form: form,
                description: description
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                message.success("上传成功").then()
                this.state.formRef.current.resetFields();
            }
        }).catch(error => {
                message.error(error).then()
            }
        )
        this.setState({
            uploading: false
        })
    }

    uploadFailed = (errorInfo) => {
        message.error(errorInfo).then()
    };

    onReset = () => {
        this.state.formRef.current.resetFields();
    }

    beforeUpload = (file) => {
        const data = new FormData();
        data.append("file", file)
        this.setState(state => ({
            fileList: [...state.fileList, file],
        }));
        sendFile("/uploadDataset", data,
            {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
                if (res.data.code === 200) {
                    setTimeout(() => {
                        this.setState(state => {
                            const index = state.fileList.indexOf(file);
                            const newFileList = state.fileList.slice();
                            newFileList.splice(index, 1);
                            return {
                                fileList: newFileList,
                            };
                        });
                    }, 500)
                } else {
                    message.error("上传失败").then()
                }
            }
        ).catch(err => {
            message.error(err).then()
        })
        return true;
    }

    onRemove = (file) => {
        this.setState(state => {
            const index = state.fileList.indexOf(file);
            const newFileList = state.fileList.slice();
            newFileList.splice(index, 1);
            return {
                fileList: newFileList,
            };
        });
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
                <Form.Item label="数据集">
                    <Upload beforeUpload={this.beforeUpload} directory onRemove={this.onRemove}
                            fileList={this.state.fileList}>
                        <Button icon={<UploadOutlined/>}>选择数据集</Button>
                    </Upload>
                </Form.Item>
                <Form.Item wrapperCol={{offset: 8, span: 16}}>
                    <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
                        <Button type="primary" htmlType="submit" loading={this.state.uploading}>
                            {this.state.uploading ? "上传中" : "上传"} </Button>
                        <Button htmlType="button" onClick={this.onReset}> 重置 </Button>
                    </div>
                </Form.Item>
            </Form>
        )
    }

}

export default UploadForm;