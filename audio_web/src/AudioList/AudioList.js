import React from "react";
import {Button, Modal, Table, message} from "antd";
import AudioDetail from "./AudioDetail";
import "antd/dist/antd.css";
import "../css/AudioList.css";
import sendGet from "../Util/axios";

class AudioList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            isModalVisible: false,
            choice: null
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
            this.setState({
                dataSource: JSON.parse(res.data.data)
            })
        }).catch(error =>
            message.error(error)
        )
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

    render() {
        return (
            <div style={{whiteSpace: "pre"}}>
                <Table columns={this.columns} dataSource={this.state.dataSource}/>
                <Modal title={this.state.choice} visible={this.state.isModalVisible} footer={null}
                       onCancel={this.handleCancel} width={1200}>
                    <AudioDetail key={this.state.choice} choice={this.state.choice}/>
                </Modal>
            </div>
        )
    }
}

export default AudioList