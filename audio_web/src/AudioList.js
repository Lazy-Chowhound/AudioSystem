import React from 'react';
import 'antd/dist/antd.css';
import './index.css';


import {Modal, Table} from 'antd';
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
            title: '音频',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: '语言',
            dataIndex: 'language',
            key: 'language',
        },
        {
            title: '大小',
            dataIndex: 'size',
            key: 'size',
        },
        {
            title: '总小时数',
            dataIndex: 'hour',
            key: 'hour',
        },
        {
            title: '录音人数',
            key: 'people',
            dataIndex: 'people',
        },
        {
            title: '格式',
            key: 'format',
            dataIndex: 'format',
        },
        {
            title: "分布",
            key: 'distribution',
            dataIndex: 'distribution',
        },
        {
            title: '音频列表',
            key: 'list',
            render: item => <button type="primary"
                                    onClick={() => {
                                        this.showDetail(item)
                                    }}>查看详细音频列表</button>,
        },
    ];

    componentDidMount() {
        const data = [
            {
                key: "1",
                name: "Chinese",
                language: "Chinese",
                size: "3GB",
                hour: 86,
                people: 3792,
                format: "MP3",
                distribution: "年龄 37% 19 - 29；12% 30 - 39；9% < 19；3% 40 - 49\n 51% 男；10% 女",
                url: "www.baidu.com"
            },
            {
                key: '2',
                name: "Japanese",
                language: "Japanese",
                size: "628MB",
                hour: 42,
                people: 1234,
                format: "MP3",
                distribution: "年龄 37% 19 - 29；12% 30 - 39；9% < 19；3% 40 - 49\n 51% 男；10% 女",
                url: "www.baidu.com"
            },
            {
                key: '3',
                name: "English",
                language: "English",
                size: "65GB",
                hour: 145,
                people: 15676,
                format: "MP3",
                distribution: "年龄 37% 19 - 29；12% 30 - 39；9% < 19；3% 40 - 49\n 51% 男；10% 女",
                url: "www.baidu.com"
            },
        ];
        this.setState({
            dataSource: data,
        })
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
            <div>
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