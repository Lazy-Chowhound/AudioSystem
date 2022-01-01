import React from 'react';
import ReactDOM from 'react-dom';
import 'antd/dist/antd.css';
import './index.css';
import {Layout, Menu, Breadcrumb} from 'antd';
import {AudioOutlined, BarsOutlined, FireOutlined} from "@ant-design/icons";

const {Header, Content, Footer, Sider} = Layout;

class SiderDemo extends React.Component {
    state = {
        collapsed: false,
        choice: "list",
    };

    onCollapse = collapsed => {
        this.setState({collapsed});
    };

    handleClick = e => {
        if (e.key === "title") {
            return;
        }
        if (e.key === "list") {
            this.setState({
                choice: "list"
            })
        } else if (e.key === "noise") {
            this.setState({
                choice: "noise"
            })
        } else if (e.key === "evaluation") {
            this.setState({
                choice: "evaluation"
            })
        }
    };

    render() {
        const {collapsed} = this.state;
        return (
            <Layout style={{minHeight: '100vh'}}>
                <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
                    <Menu theme="dark" className="menu" onClick={this.handleClick} defaultSelectedKeys={["list"]}
                          mode="inline">
                        <Menu.Item className="title" key="title">
                            音频数据集系统
                        </Menu.Item>
                        <Menu.Item key="list" icon={<BarsOutlined/>}>
                            音频列表
                        </Menu.Item>
                        <Menu.Item key="noise" icon={<AudioOutlined/>}>
                            音频扰动
                        </Menu.Item>
                        <Menu.Item key="evaluation" icon={<FireOutlined/>}>
                            质量分析
                        </Menu.Item>
                    </Menu>
                </Sider>
                <Layout className="site-layout">
                    <Header className="site-layout-background" style={{padding: 0}}/>
                    <Content style={{margin: '0 16px'}}>
                        <Breadcrumb style={{margin: '16px 0'}}>
                            <Breadcrumb.Item>User</Breadcrumb.Item>
                            <Breadcrumb.Item>Bill</Breadcrumb.Item>
                        </Breadcrumb>
                        <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                            {this.state.choice}
                        </div>
                    </Content>
                    <Footer style={{textAlign: 'center'}}>Ant Design ©2018 Created by Ant UED</Footer>
                </Layout>
            </Layout>
        );
    }
}

ReactDOM.render(<SiderDemo/>, document.getElementById("root"));
