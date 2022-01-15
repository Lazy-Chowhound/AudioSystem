import React from "react";
import {Button, Modal, Progress, Table} from "antd";
import PatternDisplay from "./PatternDisplay";
import {CloudUploadOutlined} from "@ant-design/icons";
import "../css/PerturbationAttach.css"

class PerturbationAttach extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedRowKeys: [],
            dataSource: [],
            patternChoices: [],
            percent: 30,
            visible: false
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
            render: (item) => <PatternDisplay parent={this} row={item.key}/>,
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
                this.setState({
                    visible: true
                })
                // todo 发送ajax setstate
            }
        }

    }

    handleCancel = () => {
        this.setState({
            visible: false
        })
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
                <Modal title={"处理中......"} visible={this.state.visible} footer={null}
                       width={400}
                       onCancel={this.handleCancel}>
                    <div style={{textAlign: "center"}}>
                        <Progress type="circle" percent={this.state.percent}/></div>
                </Modal>
            </div>
        );
    }
}

export default PerturbationAttach