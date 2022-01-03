import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import axios from 'axios';
import './AudioList.css';
import {Button, Modal, Table, message} from 'antd';
import AudioDetail from "./AudioDetail";

class AudioList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            isModalVisible: false
        };
    }

    columns = [
        {
            title: '音频数据集',
            dataIndex: 'name',
            key: 'name',
            align: "center"
        },
        {
            title: '语言',
            dataIndex: 'language',
            key: 'language',
            align: "center"
        },
        {
            title: '大小',
            dataIndex: 'size',
            key: 'size',
            align: "center"
        },
        {
            title: '总小时数',
            dataIndex: 'hour',
            key: 'hour',
            align: "center"
        },
        {
            title: '录音人数',
            key: 'people',
            dataIndex: 'people',
            align: "center"
        },
        {
            title: '格式',
            key: 'form',
            dataIndex: 'form',
            align: "center"
        },
        {
            title: "分布",
            key: 'distribution',
            dataIndex: 'distribution',
        },
        {
            title: '音频列表',
            key: 'list',
            render: item =>
                <Button type={"primary"} onClick={() => {
                    this.showDetail(item)
                }}>详细音频列表</Button>,
            align: "center"
        },
    ];

    componentDidMount() {
        const url = "http://localhost:8080/audioSetDescription"
        axios.get(url)
            .then(
                (response) => {
                    const data = JSON.parse(response.data.data)
                    console.log(data)
                    this.setState({
                        dataSource: data
                    })

                }
            )
            .catch((error) => {
                    message.error(error)
                }
            )

    }

    showDetail = (item) => {
        console.log(item.name)
        this.setState({
            isModalVisible: true
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
                <Modal title="Basic Modal" visible={this.state.isModalVisible} footer={null}
                       onCancel={this.handleCancel} width={700}>
                    <AudioDetail/>
                </Modal>
            </div>
        )
    }
}

export default AudioList