import React from 'react';
import 'antd/dist/antd.css';
import './index.css';


import {Table} from 'antd';

class AudioList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
        };
    }

    columns = [
        {
            title: '音频',
            dataIndex: 'name',
            key: 'name',
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
            render: url => <a href={url}>查看详细音频列表</a>,
        },
    ];

    componentDidMount() {
        const data = [
            {
                key: "1",
                name: "Chinese",
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
                size: "65GB",
                hour: 145,
                people: 15676,
                format: "MP3",
                distribution: "年龄 37% 19 - 29；12% 30 - 39；9% < 19；3% 40 - 49\n 51% 男；10% 女",
                url: "www.baidu.com"
            },
        ];
        this.setState({
            dataSource: data
        })
    }

    render() {
        return (
            <Table columns={this.columns} dataSource={this.state.dataSource}/>
        )
    }
}

export default AudioList