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
            hasUploadDataset: false,
        }
    }

    upload = (values) => {
        if (!this.state.hasUploadDataset) {
            message.error("尚未选择需要上传的数据集").then()
        } else {
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
                uploading: false,
                hasUploadDataset: false
            })
        }
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
                    this.setState({
                        hasUploadDataset: true
                    })
                } else {
                    message.error("上传失败").then()
                }
            }
        ).catch(err => {
            message.error(err).then()
        })
        return false;
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
        const size = this.state.formRef.current.getFieldsValue().size;
        if (size.length === 0) {
            return Promise.reject("大小不能为空")
        }
        if (!size.endsWith("MB") && !size.endsWith("GB") && !this.checkPositiveInteger(size.substring(0, size.length - 2))) {
            return Promise.reject("大小只能以GB或者MB结尾,且为正整数")
        }
        return Promise.resolve();
    }

    checkHour = () => {
        const hour = this.state.formRef.current.getFieldsValue().hour;
        if (hour.length === 0) {
            return Promise.reject("时长不能为空")
        }
        if (!this.checkPositiveInteger(hour)) {
            return Promise.reject("时长只能为正整数")
        }
        return Promise.resolve();
    }

    checkPeople = () => {
        const people = this.state.formRef.current.getFieldsValue().people;
        if (people.length === 0) {
            return Promise.reject("人数不能为空")
        }
        if (!this.checkPositiveInteger(people)) {
            return Promise.reject("人数只能为正整数")
        }
        return Promise.resolve();
    }

    checkForm = () => {
        const form = this.state.formRef.current.getFieldsValue().form;
        if (form.length === 0) {
            return Promise.reject("格式不能为空")
        }
        if (form !== "MP3" && form !== "WAV") {
            return Promise.reject("暂时只支持MP3和WAV")
        }
        return Promise.resolve();
    }

    checkPositiveInteger = (num) => {
        const reg = /^[1-9]\d*$/;
        return reg.test(num);
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
                           rules={[{required: true, message: ""}, {validator: this.checkSize}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="时长" name="hour"
                           rules={[{required: true, message: ""}, {validator: this.checkHour}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="人数" name="people"
                           rules={[{required: true, message: ""}, {validator: this.checkPeople}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="格式" name="form"
                           rules={[{required: true, message: ""}, {validator: this.checkForm}]}>
                    <Input/>
                </Form.Item>
                <Form.Item label="描述" name="description"
                           rules={[{required: true, message: "请输入描述"}]}>
                    <Input.TextArea/>
                </Form.Item>
                <Form.Item label="数据集">
                    <Upload beforeUpload={this.beforeUpload} directory onRemove={this.onRemove}
                            fileList={this.state.fileList}>
                        <Button icon={<UploadOutlined/>}
                                disabled={this.state.hasUploadDataset}>{this.state.hasUploadDataset ? "已上传" : "选择数据集"}
                        </Button>
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