import React from "react";
import {Table} from "antd";

class AudioDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
        };
    }

    columns = [
        {
            title: '音频名称',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: '大小',
            dataIndex: 'size',
            key: 'size',
        },
        {
            title: '单/双声道',
            dataIndex: 'channel',
            key: 'channel',
        },
        {
            title: '采样率',
            key: 'sampleRate',
            dataIndex: 'sampleRate',
        },
        {
            title: "波形图",
            key: 'distribution',
            render: item => <button type="primary"
                                    onClick={() => {
                                        this.showDetail(item)
                                    }}>波形图</button>,
        },
        {
            title: '频谱图',
            key: 'list',
            render: item => <button type="primary"
                                    onClick={() => {
                                        this.showDetail(item)
                                    }}>查看频谱图</button>,
        },
    ];

    componentDidMount() {
        const data = [
            {
                key: "1",
                name: "1.mp3",
                size: "17s",
                channel: "单",
                sampleRate: "100Hz"
            },
            {
                key: '2',
                name: "2.mp3",
                size: "8s",
                channel: "双",
                sampleRate: "90Hz"
            },
            {
                key: '3',
                name: "3.mp3",
                size: "10s",
                channel: "单",
                sampleRate: "100Hz"
            },
        ];
        this.setState({
            dataSource: data,
        })
    }

    render() {
        return (
            <Table columns={this.columns} dataSource={this.state.dataSource}/>
        )
    }
}

export default AudioDetail