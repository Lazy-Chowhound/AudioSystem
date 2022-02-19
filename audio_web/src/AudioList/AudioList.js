import React from "react";
import {Button, message, Modal, Table} from "antd";
import AudioDetail from "./AudioDetail";
import "antd/dist/antd.css";
import "../css/AudioList.css";
import sendGet from "../Util/axios";
import {UploadOutlined} from "@ant-design/icons";
import UploadForm from "./UploadForm";

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

    cancelUpload = () => {
        this.setState({
            uploadVisible: false
        })
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
                    <UploadForm uploadVisible={this.state.uploadVisible}/>
                </Modal>
            </div>
        )
    }
}

export default AudioList