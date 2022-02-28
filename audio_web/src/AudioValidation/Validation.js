import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import {Button, Drawer, message, Modal, Select, Table, Upload} from "antd";
import {getAudioSet, getAudioUrl, getNoiseAudioUrl} from "../Util/AudioUtil";
import {sendFile, sendGet} from "../Util/axios";
import {CheckOutlined, InboxOutlined, UploadOutlined} from "@ant-design/icons";
import Dragger from "antd/es/upload/Dragger";


class Validation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            loading: true,
            dataset: "",
            options: [],
            currentPage: 1,
            pageSize: 5,
            total: null,
            fileList: [],
            uploading: false,
            modelList: [],
            currentModel: null,
            preOverallWER: "",
            postOverallWER: "",
            modalVisible: false,
            historyFileList: [],
            hasSelected: false,
            drawerVisible: false
        }
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            align: "center",
        },
        {
            title: "真实文本",
            dataIndex: "realText",
            align: "center",
            ellipsis: true
        },
        {
            title: "原识别内容",
            dataIndex: "previousText",
            align: "center",
            ellipsis: true
        },
        {
            title: "原WER/CER",
            dataIndex: "preWER",
            align: "center",
            width: 100
        },
        {
            title: "现识别内容",
            dataIndex: "posteriorText",
            align: "center",
            ellipsis: true
        },
        {
            title: "现WER/CER",
            dataIndex: "postWER",
            align: "center",
            width: 100
        },
    ];

    componentDidMount() {
        getAudioSet().then(res => {
            this.setState({
                options: res,
                dataset: res[0]
            }, () => {
                this.getModels()
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    getModels = () => {
        sendGet("/models").then(res => {
            const data = JSON.parse(res.data.data)
            this.setState({
                modelList: data,
                currentModel: data[0]
            }, () => {
                this.getValidationResultsByPage()
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    getValidationResultsByPage = () => {
        this.setState({
            loading: true
        })
        sendGet("/validationResultsByPage", {
                params: {
                    audioSet: this.state.dataset,
                    model: this.state.currentModel,
                    page: this.state.currentPage,
                    pageSize: this.state.pageSize
                }
            }
        ).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
                this.setState({
                    loading: false
                })
            } else {
                const data = JSON.parse(res.data.data)
                const totalLen = data.shift().total
                const preOverallWER = data.shift().preOverallWER
                const postOverallWER = data.shift().postOverallWER
                this.setState({
                    dataSource: data,
                    total: totalLen,
                    preOverallWER: preOverallWER,
                    postOverallWER: postOverallWER,
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


    datasetChange = (e) => {
        this.setState({
            dataset: e
        }, () => {
            this.getValidationResultsByPage()
        })
    }

    modalChange = (e) => {
        this.setState({
            currentModel: e
        })
    }

    beforeUpload = (file, fileList) => {
        this.setState({
            fileList: fileList
        })
        this.setState({
            hasSelected: true
        })
        return false;
    }

    handleCancel = () => {
        this.setState({
            modalVisible: false
        })
    }

    upload = () => {
        let uploadSuccess = true;
        for (let i = 0; i < this.state.fileList.length; i++) {
            const data = new FormData();
            data.append("file", this.state.fileList[i])
            sendFile("/uploadModel", data,
                {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
                    if (res.data.code === 400) {
                        uploadSuccess = false;
                    } else {
                        this.setState(state => ({
                            historyFileList: [...state.historyFileList, this.state.fileList[i]],
                        }));
                    }
                }
            ).catch(err => {
                message.error(err).then()
            })
        }
        if (uploadSuccess) {
            message.success("上传成功").then()
        } else {
            message.error("上传失败").then()
        }
        this.setState({
            hasSelected: false,
            fileList: []
        })
    }

    showHistory = () => {
        this.setState({
            drawerVisible: true
        })
    }

    render() {
        let modalTitle =
            <div>
                <span>上传模型</span>
                <Button style={{marginLeft: 250}} onClick={this.showHistory} type={"link"}>查看上传历史</Button>
            </div>

        let summaryRow =
            <Table.Summary fixed>
                <Table.Summary.Row>
                    <Table.Summary.Cell index={0}>统 计</Table.Summary.Cell>
                    <Table.Summary.Cell index={1}>
                        <div style={{textAlign: "center"}}>
                            {`原WER/CER为 ${this.state.preOverallWER}`}
                        </div>
                    </Table.Summary.Cell>
                    <Table.Summary.Cell index={2}>
                        <div style={{textAlign: "center"}}>
                            {`现WER/CER为 ${this.state.postOverallWER}`}
                        </div>
                    </Table.Summary.Cell>
                </Table.Summary.Row>
            </Table.Summary>
        return (
            <div style={{whiteSpace: "pre", padding: 10}}>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <div>
                        <span>数据集:</span>
                        <Select value={this.state.dataset} bordered={false} size={"large"}
                                onChange={this.datasetChange}>
                            {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                    <Button icon={<UploadOutlined/>} onClick={() => {
                        this.setState({modalVisible: true})
                    }} type="primary">上传模型</Button>
                    <div>
                        <span>模型:</span>
                        <Select value={this.state.currentModel} bordered={false} onChange={this.modalChange}>
                            {this.state.modelList.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                </div>
                <Table loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showSizeChanger: false
                       }} summary={() => (summaryRow)} expandable={{
                    expandedRowRender: record => {
                        return (
                            <div>
                                <span style={{marginRight: 20}}>{"原音频:"}</span>
                                <audio
                                    src={getAudioUrl(this.state.dataset, record.name)}
                                    style={{height: 30, width: 300, verticalAlign: "middle"}}
                                    controls={true}/>
                                <span style={{marginLeft: 20, marginRight: 20}}>{"扰动音频:"}</span>
                                <audio src={getNoiseAudioUrl(this.state.dataset, record.noise_audio_name)}
                                       style={{height: 30, width: 300, verticalAlign: "middle"}}
                                       controls={true}/>
                            </div>
                        )
                    },
                    rowExpandable: () => true
                }}
                />
                <Modal visible={this.state.modalVisible} title={modalTitle} onCancel={this.handleCancel}
                       footer={[<Button type={"primary"} onClick={this.upload}>点击上传</Button>,
                           <Button onClick={this.handleCancel}>取消上传</Button>]}>
                    <Dragger beforeUpload={this.beforeUpload} directory showUploadList={false}>
                        <p className="ant-upload-drag-icon">
                            {this.state.hasSelected ? <CheckOutlined/> : <InboxOutlined/>}
                        </p>
                        <p className="ant-upload-text">{this.state.hasSelected ? "已读取目标文件" : "点击或拖拽文件到此处以上传"}</p>
                        <p className="ant-upload-hint">
                            {this.state.hasSelected ? "点击或拖拽文件重新选择" : "目前只支持上传文件夹"}
                        </p>
                    </Dragger>
                    <Drawer
                        title="Basic Drawer"
                        placement="right"
                        closable={false}
                        onClose={this.onClose}
                        visible={this.state.drawerVisible}
                        getContainer={false}
                        style={{position: 'absolute'}}
                    >
                        <p>Some contents...</p>
                    </Drawer>
                </Modal>
            </div>
        );
    }
}

export default Validation
