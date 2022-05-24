import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import {Button, Drawer, List, message, Modal, notification, Popconfirm, Select, Table} from "antd";
import {formatTime, getAudioSet, getAudioUrl, getNoiseAudioUrl} from "../Util/AudioUtil";
import {sendFile, sendGet} from "../Util/axios";
import {CheckOutlined, InboxOutlined, UploadOutlined} from "@ant-design/icons";
import Dragger from "antd/es/upload/Dragger";
import "../css/Validation.css"


class Validation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            loading: false,
            dataset: null,
            options: [],
            currentPage: 1,
            pageSize: 5,
            total: null,
            fileList: [],
            uploading: false,
            modelList: [],
            currentModel: null,
            preOverallER: 0,
            postOverallER: 0,
            modalVisible: false,
            uploadHistory: [],
            hasSelected: false,
            drawerVisible: false,
            modelName: null,
            selectedPattern: null,
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
            dataIndex: "preER",
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
            dataIndex: "postER",
            align: "center",
            width: 100
        },
    ];

    componentDidMount() {
        getAudioSet().then(res => {
            this.setState({
                options: res
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
                modelList: data
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    changePage = (page) => {
        this.setState({
            currentPage: page.current
        }, () => {
            this.getValidationResultsByPage()
        })
    }

    getValidationResultsByPage = () => {
        if (this.state.currentModel === null) {
            message.error("未选择模型").then()
            return
        }
        if (this.state.dataset === null) {
            message.error("未选择数据集").then()
            return
        }
        if (this.state.selectedPattern === null) {
            message.error("未选择类别").then()
            return
        }
        this.setState({
            loading: true
        })
        if (this.state.selectedPattern === "All") {
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
                    const preOverallER = data.shift().preOverallER
                    const postOverallER = data.shift().postOverallER
                    this.setState({
                        dataSource: data,
                        total: totalLen,
                        preOverallER: preOverallER,
                        postOverallER: postOverallER,
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
        } else {
            sendGet("/validationResultsByPattern", {
                    params: {
                        audioSet: this.state.dataset,
                        pattern: this.state.selectedPattern,
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
                    const preOverallER = data.shift().preOverallER
                    const postOverallER = data.shift().postOverallER
                    this.setState({
                        dataSource: data,
                        total: totalLen,
                        preOverallER: preOverallER,
                        postOverallER: postOverallER,
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
    }

    datasetChange = (e) => {
        this.setState({
            dataset: e
        })
    }

    patternChange = (e) => {
        this.setState({
            selectedPattern: e
        })
    }

    modalChange = (e) => {
        this.setState({
            currentModel: e
        })
    }

    beforeUpload = (file, fileList) => {
        this.setState({
            fileList: fileList,
            hasSelected: true,
            modelName: fileList[0]['webkitRelativePath'].split("/")[0]
        })
        return false;
    }

    handleCancel = () => {
        this.setState({
            modalVisible: false,
            hasSelected: false,
            fileList: []
        })
        this.getModels()
    }

    upload = async () => {
        if (this.state.fileList.length === 0) {
            message.error("尚未选择任何模型").then()
        } else if (this.state.modelName === null || this.state.modelName.length === 0) {
            message.error("请输入模型名").then()
        } else {
            this.setState({
                uploading: true
            })
            this.uploadModel().then(res => {
                if (res) {
                    this.insertUploadHistory().then(resp => {
                        if (resp) {
                            message.success("上传成功").then()
                            this.setState({
                                hasSelected: false,
                                fileList: [],
                                uploading: false,
                                modelName: null,
                            })
                        }
                    })
                }
            })
        }
    }

    insertUploadHistory = async () => {
        await sendGet("/modelHistory", {
            params: {
                model: this.state.modelName
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
                return false;
            }
        }).catch(() => {
                return false;
            }
        )
        return true;
    }

    uploadModel = async () => {
        for (let i = 0; i < this.state.fileList.length; i++) {
            const data = new FormData();
            data.append("file", this.state.fileList[i])
            await sendFile("/uploadModel", data,
                {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
                    if (res.data.code === 400) {
                        message.error(res.data.data).then()
                        return false;
                    }
                }
            ).catch(() => {
                return false;
            })
        }
        return true;
    }

    showHistory = () => {
        this.setState({
            drawerVisible: true
        }, () => {
            this.getModelUploadHistory()
        })
    }

    getModelUploadHistory = () => {
        sendGet("/uploadModelHistory").then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                const data = JSON.parse(res.data.data)
                const histories = []
                for (let i = 0; i < data.length; i++) {
                    const history = {}
                    history['key'] = data[i]['id']
                    history['name'] = data[i]['name']
                    history['time'] = formatTime(data[i]['time'])
                    histories.push(history)
                }
                this.setState({
                    uploadHistory: histories
                })
            }
        }).catch(() => {
            message.error("获取历史记录失败").then()
        })
    }

    clearHistory = () => {
        if (this.state.uploadHistory.length !== 0) {
            sendGet("/clearModelHistory").then(() => {
                notification.success({
                    message: '清空历史成功',
                    duration: 1.0
                })
                this.setState({
                    uploadHistory: []
                })
            }).catch(err => {
                message.error(err).then()
            })
        } else {
            notification.warning({
                message: '无可清空历史',
                duration: 1.0
            })
        }
    }

    closeHistory = () => {
        this.setState({
            drawerVisible: false,
        });
    };

    confirm = () => {
        this.clearHistory()
    }

    deleteHistory = (item) => {
        const name = item.name
        sendGet("/deleteModelHistory", {
            params: {
                name: name
            }
        }).then(() => {
            notification.success({
                message: '删除成功',
                duration: 1.0
            })
            this.getModelUploadHistory()
        }).catch(error => {
            message.error(error).then()
        })
    }

    startValidation = () => {
        this.setState({
            currentPage: 1
        })
        this.getValidationResultsByPage()
    }

    render() {
        let modalTitle =
            <div>
                <span>上传模型</span>
                <Button style={{marginLeft: 300}} onClick={this.showHistory} type={"link"}>查看上传历史</Button>
            </div>

        let summaryRow =
            <Table.Summary fixed>
                <Table.Summary.Row>
                    <Table.Summary.Cell index={0}>统 计</Table.Summary.Cell>
                    <Table.Summary.Cell index={1}>
                        <div style={{textAlign: "center"}}>
                            {`原WER/CER为 ${this.state.preOverallER}`}
                        </div>
                    </Table.Summary.Cell>
                    <Table.Summary.Cell index={2}>
                        <div style={{textAlign: "center"}}>
                            {`现WER/CER为 ${this.state.postOverallER}`}
                        </div>
                    </Table.Summary.Cell>
                </Table.Summary.Row>
            </Table.Summary>

        let drawerTitle =
            <div>
                <span>模型上传历史</span>
                <Popconfirm placement="leftBottom" title="确定清空？"
                            onConfirm={this.confirm} okText="确定" cancelText="取消">
                    <Button style={{marginLeft: 60}} type={"dashed"}>清空所有历史</Button>
                </Popconfirm>
            </div>

        return (
            <div style={{whiteSpace: "pre", padding: 10}}>
                <div style={{display: "flex", justifyContent: "space-between", marginBottom: "5px"}}>
                    <div>
                        <span>数据集:</span>
                        <Select placeholder="选择数据集" value={this.state.dataset} bordered={false}
                                onChange={this.datasetChange}>
                            {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                        <span>扰动类别:</span>
                        <Select placeholder="选择扰动类别" value={this.state.selectedPattern} bordered={false}
                                onChange={this.patternChange}>
                            <Select.Option key={"All"} value={"All"}/>
                            <Select.Option key={"Gaussian noise"} value={"Gaussian noise"}/>
                            <Select.Option key={"Sound level"} value={"Sound level"}/>
                            <Select.Option key={"Animal"} value={"Animal"}/>
                            <Select.Option key={"Source-ambiguous sounds"} value={"Source-ambiguous sounds"}/>
                            <Select.Option key={"Natural sounds"} value={"Natural sounds"}/>
                            <Select.Option key={"Sound of things"} value={"Sound of things"}/>
                            <Select.Option key={"Human sounds"} value={"Human sounds"}/>
                            <Select.Option key={"Music"} value={"Music"}/>
                        </Select>
                    </div>
                    <Button icon={<UploadOutlined/>} onClick={() => {
                        this.setState({modalVisible: true})
                    }} type="primary">上传模型</Button>
                    <div>
                        <span>模型:</span>
                        <Select placeholder="选择模型" value={this.state.currentModel} bordered={false}
                                onChange={this.modalChange}>
                            {this.state.modelList.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                </div>
                <Table rowClassName={(record) => {
                    if (parseFloat(record.postER) - parseFloat(record.preER) > 0) {
                        return "wrong_row"
                    } else {
                        return "right_row"
                    }
                }}
                       loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showSizeChanger: false
                       }} onChange={this.changePage} summary={() => (summaryRow)} expandable={{
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
                <Button style={{marginTop: "20px"}} type={"primary"} onClick={this.startValidation}>开始验证</Button>
                <Modal visible={this.state.modalVisible} title={modalTitle} onCancel={this.handleCancel}
                       footer={[<Button type={"primary"} onClick={this.upload}
                                        loading={this.state.uploading}>{this.state.uploading ? "上传中" : "点击上传"}</Button>,
                           <Button onClick={this.handleCancel}>取消上传</Button>]} width={550}>
                    <div>模型名称: {this.state.modelName}</div>
                    <Dragger style={{marginTop: "20px", height: "400px"}} beforeUpload={this.beforeUpload} directory
                             showUploadList={false}>
                        <p className="ant-upload-drag-icon">
                            {this.state.hasSelected ? <CheckOutlined/> : <InboxOutlined/>}
                        </p>
                        <p className="ant-upload-text">{this.state.hasSelected ? "已读取目标文件" : "点击或拖拽文件到此处以上传"}</p>
                        <p className="ant-upload-hint">
                            {this.state.hasSelected ? "点击或拖拽文件重新选择" : "目前只支持上传文件夹"}
                        </p>
                    </Dragger>
                </Modal>
                <Drawer title={drawerTitle} placement="right" onClose={this.closeHistory}
                        visible={this.state.drawerVisible}>
                    <List itemLayout="horizontal" dataSource={this.state.uploadHistory}
                          renderItem={item => (
                              <List.Item actions={[<Button type={"link"} onClick={() => {
                                  this.deleteHistory(item)
                              }}>删除此条</Button>]}>
                                  <List.Item.Meta title={item.name} description={item.time}/>
                              </List.Item>
                          )}/>
                </Drawer>
            </div>
        );
    }
}

export default Validation
