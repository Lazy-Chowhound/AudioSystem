import React from "react";
import {Button, Drawer, List, message, Modal, notification, Popconfirm, Table} from "antd";
import AudioDetail from "./AudioDetail";
import "antd/dist/antd.css";
import "../css/AudioList.css";
import {sendGet} from "../Util/axios";
import {UploadOutlined} from "@ant-design/icons";
import UploadForm from "./UploadForm";
import {formatTime} from "../Util/AudioUtil";

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
            drawerVisible: false,
            uploadHistory: []
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
            align: "center",
        },
        {
            title: "大小",
            dataIndex: "size",
            align: "center",
            width: 80
        },
        {
            title: "总小时数",
            dataIndex: "hour",
            align: "center",
            width: 80
        },
        {
            title: "录音人数",
            dataIndex: "people",
            align: "center",
            width: 80
        },
        {
            title: "格式",
            dataIndex: "form",
            align: "center",
            width: 70
        },
        {
            title: "描述",
            dataIndex: "description",
            width: 500,
            ellipsis: true
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
        this.getAudioSetProperties()
    }

    getAudioSetProperties = () => {
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

    cancelUpload = () => {
        this.setState({
            uploadVisible: false
        })
        this.getAudioSetProperties()
    }

    showHistory = () => {
        this.setState({
            drawerVisible: true
        }, () => {
            this.getDatasetUploadHistory()
        })
    }

    getDatasetUploadHistory = () => {
        sendGet("/uploadDatasetHistory").then(res => {
            if (res.data.code === 400) {
                message.error("没有相关权限").then()
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

    confirm = () => {
        this.clearHistory()
    }

    clearHistory = () => {
        if (this.state.uploadHistory.length !== 0) {
            sendGet("/clearDatasetHistory").then(res => {
                if (res.data.code === 400) {
                    message.error("没有相关权限").then()
                } else {
                    notification.success({
                        message: '清空历史成功',
                        duration: 1.0
                    })
                    this.setState({
                        uploadHistory: []
                    })
                }
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

    deleteHistory = (item) => {
        const name = item.name
        sendGet("/deleteDatasetHistory", {
            params: {
                name: name
            }
        }).then(() => {
            notification.success({
                message: '删除成功',
                duration: 1.0
            })
            this.getDatasetUploadHistory()
        }).catch(error => {
            message.error(error).then()
        })
    }

    render() {
        let modalTitle =
            <div>
                <span>数据集上传</span>
                <Button style={{marginLeft: 230}} onClick={this.showHistory} type={"link"}>查看上传历史</Button>
            </div>

        let drawerTitle =
            <div>
                <span>数据集上传历史</span>
                <Popconfirm placement="leftBottom" title="确定清空？"
                            onConfirm={this.confirm} okText="确定" cancelText="取消">
                    <Button style={{marginLeft: 60}} type={"dashed"}>清空所有历史</Button>
                </Popconfirm>
            </div>

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
                <Modal style={{marginTop: -70}} visible={this.state.uploadVisible} width={500}
                       title={modalTitle} footer={[<Button key="back" onClick={this.cancelUpload}>取消上传</Button>]}
                       onCancel={this.cancelUpload}>
                    <UploadForm uploadVisible={this.state.uploadVisible}/>
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
        )
    }
}

export default AudioList