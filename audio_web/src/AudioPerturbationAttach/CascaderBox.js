import React from "react";
import {Cascader} from "antd";

class CascaderBox extends React.Component {
    options = [
        {
            value: 'zhejiang',
            label: 'Zhejiang',
            children: [
                {
                    value: 'hangzhou',
                    label: 'Hangzhou',
                    children: [
                        {
                            value: 'xihu',
                            label: 'West Lake',
                        },
                    ],
                },
            ],
        },
        {
            value: 'jiangsu',
            label: 'Jiangsu',
            children: [
                {
                    value: 'nanjing',
                    label: 'Nanjing',
                    children: [
                        {
                            value: 'zhonghuamen',
                            label: 'Zhong Hua Men',
                        },
                    ],
                },
            ],
        },
    ];

    onChange = (value) => {
        console.log(value);
    }

    render() {
        return (
            <Cascader options={this.options} onChange={this.onChange} placeholder="Please select"/>
        )
    }
}

export default CascaderBox