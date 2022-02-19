import React from "react";
import {Button, Form, Input, message, Modal, Table, Upload} from "antd";
import AudioDetail from "./AudioDetail";
import "antd/dist/antd.css";
import "../css/AudioList.css";
import sendGet from "../Util/axios";
import {UploadOutlined} from "@ant-design/icons";

class AudioList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            isModalVisible: false,
            choice: null,
            total: null,
            currentPage: 1,
            pageSize: 3,
            loading: true,
            uploadVisible: false,
            formRef: React.createRef()
        };
    }

    columns = [
        {
            title: "音频数据集",
            dataIndex: "name",
            align: "center"
        },
        {
            title: "语言",
            dataIndex: "language",
            align: "center"
        },
        {
            title: "大小",
            dataIndex: "size",
            align: "center"
        },
        {
            title: "总小时数",
            dataIndex: "hour",
            align: "center"
        },
        {
            title: "录音人数",
            dataIndex: "people",
            align: "center"
        },
        {
            title: "格式",
            dataIndex: "form",
            align: "center"
        },
        {
            title: "分布",
            dataIndex: "distribution",
        },
        {
            title: "音频列表",
            render: (text, record) =>
                <Button type={"primary"} onClick={() => {
                    this.showDetail(record.name)
                }}>详细音频列表</Button>,
            align: "center"
        },
    ];

    componentDidMount() {
        sendGet("/audioSetsProperties").then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
                this.setState({
                    loading: false
                })
            } else {
                const data = JSON.parse(res.data.data)
                this.setState({
                    total: data.length,
                    dataSource: data,
                    loading: false
                })
            }
        }).catch(error => {
                message.error(error).then()
                this.setState({
                    loading: false
                })
            }
        )
    }

    showDetail = (name) => {
        this.setState({
            isModalVisible: true,
            choice: name
        })
    }

    handleCancel = () => {
        this.setState({
            isModalVisible: false
        })
    }

    uploadDataset = () => {
        this.setState({
            uploadVisible: true
        })
    }

    upload = (values) => {
        console.log(values)
    }

    uploadFailed = (errorInfo) => {
        console.log(errorInfo);
    };

    cancelUpload = () => {
        this.setState({
            uploadVisible: false
        })
    }

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
            <div style={{whiteSpace: "pre"}}>
                <Button style={{margin: 10}} type="primary" shape="round" icon={<UploadOutlined/>}
                        onClick={this.uploadDataset}>
                    上传数据集
                </Button>
                <Table loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showSizeChanger: false
                       }}/>
                <Modal style={{marginTop: -90}} title={this.state.choice} visible={this.state.isModalVisible}
                       footer={null} onCancel={this.handleCancel} width={1200}>
                    <AudioDetail key={this.state.choice} choice={this.state.choice}/>
                </Modal>
                <Modal style={{marginTop: -50}} visible={this.state.uploadVisible} width={500}
                       title="数据集上传" footer={[<Button key="back" onClick={this.cancelUpload}>取消上传</Button>]}
                       onCancel={this.cancelUpload}>
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
                </Modal>
            </div>
        )
    }
}

export default AudioList