import React from "react";
import {Button, message, Modal, Table} from "antd";
import AudioDetail from "./AudioDetail";
import "antd/dist/antd.css";
import "../css/AudioList.css";
import sendGet from "../Util/axios";

class AudioList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            audioSet: [],
            dataSource: [],
            isModalVisible: false,
            choice: null,
            total: null,
            page: 1,
            pageSize: 4,
            loading: true,
        };
    }

    columns = [
        {
            title: "音频数据集",
            dataIndex: "name",
            key: "name",
            align: "center"
        },
        {
            title: "语言",
            dataIndex: "language",
            key: "language",
            align: "center"
        },
        {
            title: "大小",
            dataIndex: "size",
            key: "size",
            align: "center"
        },
        {
            title: "总小时数",
            dataIndex: "hour",
            key: "hour",
            align: "center"
        },
        {
            title: "录音人数",
            key: "people",
            dataIndex: "people",
            align: "center"
        },
        {
            title: "格式",
            key: "form",
            dataIndex: "form",
            align: "center"
        },
        {
            title: "分布",
            key: "distribution",
            dataIndex: "distribution",
        },
        {
            title: "音频列表",
            key: "list",
            render: item =>
                <Button type={"primary"} onClick={() => {
                    this.showDetail(item)
                }}>详细音频列表</Button>,
            align: "center"
        },
    ];

    componentDidMount() {
        sendGet("/audioSetDescription").then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                const data = JSON.parse(res.data.data)
                this.setState({
                    audioSet: data,
                    total: Math.ceil(data.length / (this.state.pageSize - 1)) * this.state.pageSize,
                    dataSource: data.slice(0, this.state.pageSize - 1),
                })
            }
        }).catch(error => {
                message.error(error).then()
            }
        )
        this.setState({
            loading: false
        })
    }

    showDetail = (item) => {
        this.setState({
            isModalVisible: true,
            choice: item.name
        })
    }

    handleCancel = () => {
        this.setState({
            isModalVisible: false
        })
    }

    onChange = (page) => {
        this.setState({
            currentPage: page.current
        }, () => {
            this.setState({
                dataSource: this.state.audioSet.slice((this.state.currentPage - 1) * (this.state.pageSize - 1),
                    Math.min(this.state.currentPage * this.state.pageSize - this.state.currentPage, this.state.total))
            })
        })
    }

    render() {
        return (
            <div style={{whiteSpace: "pre"}}>
                <Table loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showSizeChanger: false
                       }} onChange={this.onChange}/>
                <Modal title={this.state.choice} visible={this.state.isModalVisible} footer={null}
                       onCancel={this.handleCancel} width={1200}>
                    <AudioDetail key={this.state.choice} choice={this.state.choice}/>
                </Modal>
            </div>
        )
    }
}

export default AudioList