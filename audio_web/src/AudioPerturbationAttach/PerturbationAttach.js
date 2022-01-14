import React from "react";
import {Table} from "antd";
import CascaderBox from "./CascaderBox";


class PerturbationAttach extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedRowKeys: [],
            dataSource: []
        };
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            align: "center"
        },
        {
            title: "扰动类型",
            dataIndex: "pattern",
            align: "center"
        },
        {
            title: "具体扰动",
            dataIndex: "patternType",
            align: "center"
        },
        {
            title: "更改扰动",
            dataIndex: "choicePattern",
            render: () => <CascaderBox/>,
            align: "center"
        }
    ];

    componentDidMount() {
        const d = []
        for (let i = 0; i < 46; i++) {
            d.push({
                key: i,
                name: "mp3 " + i,
                pattern: "Sound level",
                patternType: "louder",
            });
        }
        this.setState({
            dataSource: d
        })
    }

    onSelectChange = (selectedRowKeys) => {
        this.setState({
            selectedRowKeys: selectedRowKeys
        });
    };

    render() {
        const {selectedRowKeys} = this.state;
        const locales = {selectionAll: "全选", selectNone: "清空所有"}
        const rowSelection = {
            selectedRowKeys,
            onChange: this.onSelectChange,
            selections: [
                Table.SELECTION_ALL,
                Table.SELECTION_NONE
            ],
        };
        return (
            <div>
                <Table rowSelection={rowSelection} columns={this.columns}
                       dataSource={this.state.dataSource} locale={locales}
                       summary={() => (
                           <Table.Summary fixed>
                               <Table.Summary.Row>
                                   <Table.Summary.Cell index={0}>Summary</Table.Summary.Cell>
                                   <Table.Summary.Cell
                                       index={1}>{selectedRowKeys.length >= 10 ? `Selected ${selectedRowKeys.length} items` :
                                       `Selected 0${selectedRowKeys.length} items`}</Table.Summary.Cell>
                               </Table.Summary.Row>
                           </Table.Summary>
                       )}/>
            </div>
        );
    }
}

export default PerturbationAttach