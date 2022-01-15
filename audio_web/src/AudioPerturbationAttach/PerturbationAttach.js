import React from "react";
import {Button, Modal, Table} from "antd";
import CascaderBox from "./CascaderBox";
import {CloudUploadOutlined} from "@ant-design/icons";


class PerturbationAttach extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedRowKeys: [],
            dataSource: [],
            patternChoices: []
        };
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            key: "name",
            align: "center",
            width: 320
        },
        {
            title: "扰动类型",
            dataIndex: "pattern",
            align: "center",
        },
        {
            title: "具体扰动",
            dataIndex: "patternType",
            align: "center",
        },
        {
            title: "添加/更改扰动",
            render: (item) => <CascaderBox parent={this} row={item.key}/>,
            align: "center"
        }
    ];

    componentDidMount() {
        const d = []
        for (let i = 0; i < 46; i++) {
            d.push({
                key: i,
                name: "mp3 " + i,
                pattern: "Sounds of things",
                patternType: "Miscellaneous sources",
            });
        }
        this.setState({
            dataSource: d
        })
    }

    getChildren = (children, option) => {
        const choices = this.state.patternChoices
        choices.push(option)
        this.setState({
            patternChoices: choices
        })
    }

    onSelectChange = (selectedRowKeys) => {
        this.setState({
            selectedRowKeys: selectedRowKeys
        });
    };

    handleClick = () => {
        const choices = this.state.patternChoices
        const selectedKeys = this.state.selectedRowKeys
        if (selectedKeys.length === 0) {
            Modal.warning({
                title: "警告",
                content: "您尚未选择任何音频",
            });
        } else {
            let count = 0;
            for (let i = 0; i < selectedKeys.length; i++) {
                for (let j = 0; j < choices.length; j++) {
                    if (choices[j][0] === selectedKeys[i]) {
                        count++;
                        break;
                    }
                }
                if (count !== i + 1) {
                    Modal.error({
                        title: "警告",
                        content: "选中行的 添加/更改扰动 为必选项",
                    });
                    break;
                }
            }
            if (count === selectedKeys.length) {
                alert("ok");
            }
        }
    }

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
                                   <Table.Summary.Cell index={1}>
                                       <div style={{textAlign: "center"}}>{selectedRowKeys.length >= 10 ?
                                           `${selectedRowKeys.length} items selected / total ${this.state.dataSource.length} items` :
                                           `${selectedRowKeys.length} items selected / total ${this.state.dataSource.length} items`}
                                       </div>
                                   </Table.Summary.Cell>
                                   <Table.Summary.Cell index={2}>
                                       <div style={{textAlign: "center"}}>
                                           <Button type="primary" shape="round" icon={<CloudUploadOutlined/>}
                                                   onClick={() => {
                                                       this.handleClick()
                                                   }}>
                                               确认提交
                                           </Button></div>
                                   </Table.Summary.Cell>
                               </Table.Summary.Row>
                           </Table.Summary>
                       )}
                />
            </div>
        );
    }
}

export default PerturbationAttach